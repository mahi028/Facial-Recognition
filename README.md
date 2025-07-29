# Facial Recognition App

A modern web-based facial recognition application built with Flask and InsightFace. This application allows users to register with multiple face images and later recognize them using a single image.

## Features

- **User Registration**: Register users with at least 4 face images for accurate recognition
- **Face Recognition**: Identify registered users using a single face image
- **Modern UI**: Bootstrap-based responsive interface with smooth animations
- **Real-time Processing**: Fast face detection and recognition using InsightFace
- **Similarity Scoring**: Shows confidence scores for recognition results


## Prerequisites
This application currently **only supports Linux environments**.

Before running the backend application, you need to install the following dependencies:

```sh
sudo apt install cmake
python3 -m pip install --upgrade pip setuptools wheel
```

## Setup and Installation

1. Create and Activate Virtual Environment (Optional):
```sh
python3 -m venv env
source env/bin/activate
```

2. Install Python dependencies:
```sh
python3.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

To start the backend server:

```sh
python3 run.py
```

## Environment Requirements

- **Operating System**: Linux (Ubuntu/Debian recommended)
- **Python**: 3.7 or higher
- **CMake**: Required for certain Python packages

## Notes

- Make sure all prerequisites are installed before attempting to run the application
- The application may not work properly on Windows or macOS due to Linux-specific dependencies
- If you encounter any installation issues, ensure your system is up to date: `sudo apt update && sudo apt upgrade`

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
