import cv2
import torch
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 face detection model globally (best for performance)
model = YOLO("yolov8n-face.pt").to('cuda' if torch.cuda.is_available() else 'cpu')

def tight_crop(face_img):
    """Optional: Further crop face to remove extra areas like hair, background."""
    h, w, _ = face_img.shape
    cropped_face = face_img[int(0.1 * h):int(0.9 * h), int(0.1 * w):int(0.9 * w)]
    return cv2.resize(cropped_face, (100, 100))

def detect_faces(frame, draw_box=True, conf_threshold=0.5):
    results = model(frame)

    faces = []
    face_coords = []

    for box, conf in zip(results[0].boxes.xyxy.cpu().numpy(), results[0].boxes.conf.cpu().numpy()):
        if conf < conf_threshold:
            continue

        x1, y1, x2, y2 = map(int, box)
        face_img = frame[y1:y2, x1:x2]

        face_img = tight_crop(face_img)
        faces.append(face_img)
        face_coords.append((x1, y1, x2 - x1, y2 - y1))

        if draw_box:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Conf: {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # ✅ Return empty list instead of None if no faces detected
    return frame, faces, face_coords
