import face_recognition as fr  
import cv2  
import numpy as np
import sys

def enhance_image(image):
    """Enhance brightness & contrast for better face detection."""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    equalized = cv2.equalizeHist(gray)
    return cv2.cvtColor(equalized, cv2.COLOR_GRAY2RGB)

def detect_faces_with_opencv(image_path):
    """Use OpenCV Haarcascades as a fallback to detect faces."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return [(y, x+w, y+h, x) for (x, y, w, h) in faces]

def load_and_process_image(image_path):
    """Load, convert, enhance, and resize image for better face detection."""
    image = fr.load_image_file(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    enhanced_image = enhance_image(rgb_image)
    return cv2.resize(enhanced_image, (0, 0), fx=1.5, fy=1.5)  # Slight upscale

# Input image paths
one = sys.argv[1]
two = sys.argv[2]

# Load and process images
RgbFaceOne = load_and_process_image(one)
RgbFaceTwo = load_and_process_image(two)

# Detect faces using HOG first
faceLocOne = fr.face_locations(RgbFaceOne, model="hog")
faceLocTwo = fr.face_locations(RgbFaceTwo, model="hog")

# If HOG fails, try OpenCV Haarcascade
if not faceLocOne:
    faceLocOne = detect_faces_with_opencv(one)
if not faceLocTwo:
    faceLocTwo = detect_faces_with_opencv(two)

# Ensure faces are detected
if not faceLocOne or not faceLocTwo:
    print("0")  # No face detected, return 0
    exit()

# Use only the first detected face
faceLocOne = faceLocOne[0]
faceLocTwo = faceLocTwo[0]

# Encode faces
encodingsOne = fr.face_encodings(RgbFaceOne, [faceLocOne])
encodingsTwo = fr.face_encodings(RgbFaceTwo, [faceLocTwo])

# Ensure encodings exist
if not encodingsOne or not encodingsTwo:
    print("0")  # Could not encode faces, return 0
    exit()

faceOneEnco = encodingsOne[0]
faceTwoEnco = encodingsTwo[0]

# Compute face similarity
face_distance = fr.face_distance([faceOneEnco], faceTwoEnco)[0]
threshold = 0.5  # Adjust as needed

# Determine match
MatchResult = int(face_distance < threshold)
print(MatchResult)  # Print 1 (match) or 0 (no match)
