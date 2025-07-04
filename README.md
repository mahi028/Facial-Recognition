# Facial Recognition App

A modern web-based facial recognition application built with Flask and InsightFace. This application allows users to register with multiple face images and later recognize them using a single image.

## Features

- **User Registration**: Register users with at least 4 face images for accurate recognition
- **Face Recognition**: Identify registered users using a single face image
- **Modern UI**: Bootstrap-based responsive interface with smooth animations
- **Real-time Processing**: Fast face detection and recognition using InsightFace
- **Similarity Scoring**: Shows confidence scores for recognition results

## Installation

1. **Create Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   Open your browser and go to: `http://localhost:5000`

## Usage

### Registration
1. Go to the "Register New User" tab
2. Fill in the user details (User ID, Name, Email)
3. Upload at least 4 clear face images from different angles
4. Click "Register User"

### Recognition
1. Go to the "Recognize User" tab
2. Upload a single clear face image
3. Click "Recognize Face"
4. View the recognition results with similarity scores

## Technical Details

- **Face Detection**: Uses InsightFace's Buffalo_L model
- **Face Embedding**: 512-dimensional face embeddings
- **Similarity Search**: FAISS index for fast similarity search
- **Database**: SQLite for storing user data and embeddings
- **Recognition Threshold**: 45% similarity threshold for matches

## API Endpoints

- `POST /register`: Register a new user with face images
- `POST /recognize`: Recognize a face from an uploaded image
- `GET /`: Main web interface

## File Structure

```
├── app.py                 # Main Flask application
├── templates/
│   └── index.html         # Web interface template
├── static/
│   ├── js/
│   │   └── app.js         # Frontend JavaScript
│   └── css/
│       └── style.css      # Custom CSS styles
├── instance/
│   └── face_db.sqlite     # SQLite database
└── requirements.txt       # Python dependencies
```

## Requirements

- Python 3.7+
- OpenCV compatible system
- At least 4GB RAM for face processing
- Modern web browser for the interface

## Notes

- Images should contain clear, well-lit faces
- Multiple faces in an image will use the largest detected face
- The system works best with frontal face images
- Supported image formats: JPG, PNG, JPEG
