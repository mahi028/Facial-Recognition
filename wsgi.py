from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import insightface
import numpy as np
import faiss
import io
import pickle
from PIL import Image

# === Flask and DB Setup ===
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///face_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
db = SQLAlchemy(app)

# Add CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# === Models ===
class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

class Embedding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    vector = db.Column(db.LargeBinary, nullable=False)

# === Face + FAISS Setup ===
face_model = insightface.app.FaceAnalysis(name='buffalo_l')
face_model.prepare(ctx_id=0)  # set to -1 if using CPU

embedding_dim = 512
faiss_index = faiss.IndexFlatIP(embedding_dim)  # cosine similarity
user_ids = []

def extract_embedding(image_bytes):
    """Extract face embedding from image bytes"""
    try:
        img = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
        faces = face_model.get(img)
        if not faces:
            return None
        
        # Get the largest face if multiple faces detected
        if len(faces) > 1:
            face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
        else:
            face = faces[0]
            
        emb = face.embedding
        emb = emb / np.linalg.norm(emb)  # normalize
        return emb.astype(np.float32)
    except Exception as e:
        print(f"Error extracting embedding: {e}")
        return None

def reload_faiss():
    user_ids.clear()
    faiss_index.reset()

    all_embeddings = []
    for record in Embedding.query.all():
        emb = pickle.loads(record.vector)
        all_embeddings.append(emb)
        user_ids.append(record.user_id)

    if all_embeddings:
        faiss_index.add(np.vstack(all_embeddings))

# === API Routes ===

@app.route('/')
def index():
    """Serve the main interface"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/register', methods=['POST'])
def register():
    try:
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        email = request.form.get('email')
        files = request.files.getlist('images')

        if not all([user_id, name, email]):
            return jsonify({"error": "Missing required fields: user_id, name, and email are required"}), 400

        if not files or len(files) < 4:
            return jsonify({"error": "Please upload at least 4 face images for better recognition accuracy"}), 400

        embeddings = []
        processed_images = 0
        
        for file in files:
            if file.filename == '':
                continue
                
            try:
                emb = extract_embedding(file.read())
                if emb is not None:
                    embeddings.append(emb)
                    processed_images += 1
            except Exception as e:
                print(f"Error processing image {file.filename}: {e}")
                continue

        if not embeddings:
            return jsonify({"error": "No valid face detected in any image. Please ensure images contain clear, visible faces"}), 400

        if len(embeddings) < 2:
            return jsonify({"error": "At least 2 images with valid faces are required for registration"}), 400

        # Save user and embeddings
        user = User(id=user_id, name=name, email=email)
        db.session.merge(user)  # upsert

        # Clear existing embeddings for this user
        Embedding.query.filter_by(user_id=user_id).delete()

        for emb in embeddings:
            blob = pickle.dumps(emb)
            db.session.add(Embedding(user_id=user_id, vector=blob))

        db.session.commit()
        reload_faiss()

        return jsonify({
            "message": f"User {user_id} registered successfully with {len(embeddings)} face embeddings",
            "user_id": user_id,
            "name": name,
            "processed_images": processed_images
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500
@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        file = request.files.get('image')
        if not file or file.filename == '':
            return jsonify({"error": "No image uploaded"}), 400

        emb = extract_embedding(file.read())
        if emb is None:
            return jsonify({"error": "No face detected in the uploaded image. Please upload a clear image with a visible face"}), 400

        if len(user_ids) == 0:
            return jsonify({"error": "No users registered in the system yet"}), 404

        emb = emb.reshape(1, -1)
        k = min(10, len(user_ids))  # search top k embeddings
        scores, indices = faiss_index.search(emb, k=k)

        THRESHOLD = 0.45
        user_scores = {}  # user_id -> best similarity

        for score, idx in zip(scores[0], indices[0]):
            if idx >= len(user_ids) or score < THRESHOLD:
                continue
            user_id = user_ids[idx]
            if user_id not in user_scores or score > user_scores[user_id]:
                user_scores[user_id] = score

        # Sort users by similarity
        top_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)[:3]

        if not top_users:
            return jsonify({
                "error": "No matching user found", 
                "message": "The face in the image doesn't match any registered users",
                "top_similarity": float(scores[0][0]) if len(scores[0]) > 0 else 0
            }), 404

        results = []
        for user_id, similarity in top_users:
            user = User.query.get(user_id)
            if user:
                results.append({
                    "user_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "similarity": float(similarity)
                })

        return jsonify({"matches": results})
        
    except Exception as e:
        return jsonify({"error": f"Recognition failed: {str(e)}"}), 500

# === Init DB and FAISS ===
with app.app_context():
    db.create_all()
    reload_faiss()

if __name__ == '__main__':
    app.run(debug=True)
