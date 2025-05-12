import os
import cv2
import utils
import numpy as np
import face_detection
import time
import threading
import subprocess
from keras.models import load_model
import smtplib
import geocoder
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from geopy.geocoders import Nominatim
from email import encoders
from queue import Queue
import tkinter as tk
from PIL import Image, ImageTk
import sys

def main(r, img, name):
    print(f"Trying to load image from: {img}")
    print(f" ")
    print(f"{img}, {r}")
    print(f" ")
    print(f"{name}")
    print(f" ")
    print(f"{r}")
    try:
        # Load Model
        model = load_model('siamese_nn.h5', custom_objects={'contrastive_loss': utils.contrastive_loss, 'euclidean_distance': utils.euclidean_distance})
        print("Model loaded successfully.")
    except Exception as e:
        print("Error loading the model:", e)
        return

 

    try:
        # Load True Image
        true_img = cv2.imread(img, 0)
        if true_img is None:
            raise FileNotFoundError(f"Image not found at: {img}")

        true_img = cv2.resize(true_img, (100, 100))
        true_img = true_img.astype('float32') / 255
        true_img = true_img.reshape(1, 100, 100, 1)
        print("True image loaded and processed successfully.")
    except Exception as e:
        print("Error loading or processing the true image:", e)
        return

    # Thresholds
    THRESHOLD = 0.55
    RECOGNITION_INTERVAL = 5 # Run every 4 sec
    last_recognition_times = [0] * 4  # Track last recognition time for each camera

    # Create Queue for Face Processing
    face_queue = Queue()

    # Create directory for recognized faces
    if not os.path.exists("recognized_faces"):
        os.makedirs("recognized_faces")

    # Open four camera feeds
    cameras = [cv2.VideoCapture(i) for i in range(4)]

    # Create Tkinter window
    root = tk.Tk()
    root.title("Multi-Camera Face Recognition")

    # Create labels for displaying video feeds
    labels = [tk.Label(root) for _ in range(4)]
    for i, label in enumerate(labels):
        label.grid(row=i // 2, column=i % 2)

    # Create labels for camera numbers
    cam_labels = [tk.Label(root, text=f"Camera {i}", font=("Arial", 12, "bold")) for i in range(4)]
    for i, cam_label in enumerate(cam_labels):
        cam_label.grid(row=i // 2, column=i % 2, sticky="n")

    # Dictionary to hold references to the images
    image_references = {}

    def update_camera_feed():
        """Update the four camera feeds in the Tkinter window."""
        nonlocal last_recognition_times
        current_time = time.time()

        for i, cam in enumerate(cameras):
            ret, frame = cam.read()

            if not ret:
                print(f"Failed to read frame from Camera {i}.")
                continue

            try:
                frame = cv2.resize(frame, (320, 240))
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

                # Maintain a strong reference to the image
                image_references[f"cam_{i}"] = img
                labels[i].config(image=image_references[f"cam_{i}"])
                #print(f"Camera {i} feed updated successfully.")

                if current_time - last_recognition_times[i] >= RECOGNITION_INTERVAL:
                    print(f"Processing frame from Camera {i} for face recognition.")
                    process_frame(frame, i)
                    last_recognition_times[i] = current_time

            except Exception as e:
                print(f"Error updating Camera {i} feed:", e)

        root.after(10, update_camera_feed)  # Update every 10ms

    def process_frame(frame, cam_number):
        """Detect and process faces from the frame."""
        small_frame = cv2.resize(frame, (320, 240))
        small_frame, faces, face_coords_list = face_detection.detect_faces(small_frame, draw_box=False)

        print(f"Detected {len(faces)} faces from Camera {cam_number}.")

        if faces:
            highest_similarity = 0
            best_match = None
            recognized_image_path = None

            for i, face_img in enumerate(faces):
                if isinstance(face_img, np.ndarray) and face_img.size > 0:
                    try:
                        face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                        face_gray = cv2.resize(face_gray, (100, 100))
                        face_gray = face_gray.astype('float32') / 255
                        face_gray = face_gray.reshape(1, 100, 100, 1)

                        similarity = 1 - model.predict([true_img, face_gray])[0][0]
                        print(f"Similarity with True Image: {similarity:.2f}")

                        if similarity > highest_similarity:
                            highest_similarity = similarity
                            best_match = face_coords_list[i]

                    except Exception as e:
                        print("Error during face comparison:", e)

            if best_match and highest_similarity >= THRESHOLD:
                x, y, w, h = best_match
                recognized_image_path = f"recognized_faces/face_{int(time.time())}.jpg"
                face_crop = frame[y:y + h, x:x + w].copy()
                cv2.imwrite(recognized_image_path, face_crop)
                face_queue.put((recognized_image_path, cam_number))

    def process_faces():
        """Background thread to handle face verification and email notifications."""
        while True:
            face_path, cam_number = face_queue.get()
            if os.path.exists(face_path):
                print(f"Processing recognized face: {face_path}")
                decision = secondary_face_verification(face_path)
                if decision == 1:
                    print(f"---------------------Match confirmed from Camera ------------------✅✅✅✅✅✅✅✅✅✅{cam_number}: {face_path}")
                    send_email(face_path,cam_number)
                else:
                    print(f"-------------------No match from Camera--------------------❌❌❌❌❌❌❌ {cam_number}: {face_path}")
                try:
                    #os.remove(face_path)
                    print(f"Deleted processed face image: {face_path}")
                except Exception as e:
                    print(f"Error deleting file {face_path}: {e}")
                else:
                    print("Error: Recognized face image not found:", face_path)

            face_queue.task_done()

    def secondary_face_verification(image_path):
        try:
            result = subprocess.run(["python", "face_verify.py", image_path, "true_img.png"], capture_output=True, text=True)
            return int(result.stdout.strip()) if result.stdout.strip().isdigit() else -1
        except Exception as e:
            print("Verification error:", e)
            return -1

    def send_email(recognized_image_path,am_number,recipient=r):
        """Sends an email with the recognized face and location."""
        try:
            g = geocoder.ip('me')  # Get location
            location = g.latlng if g.ok else "Unknown"
            if location != "Unknown":
                geolocator = Nominatim(user_agent="trinetra")
                address = geolocator.reverse(location, language="en")
                location_str = address.address if address else "Unknown"
                cam_number=am_number
            else:
                location_str = "Unknown"

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            subject = f"Trinetra Alert: {name} Recognized"

            body = f"""
            <html>
            <body style="font-family: 'Courier New', sans-serif; background-color: #0d0d24; color: #e600ff; padding: 20px;">
                <div style="max-width: 500px; margin: auto; background: linear-gradient(135deg, #1a1a40, #330033); padding: 20px; border-radius: 10px; box-shadow: 0px 0px 15px rgba(230, 0, 255, 0.5); border: 1px solid #6600cc;">
                    <h2 style="text-align: center; color: #00e6e6; margin-bottom: 10px;">🚨 SUSPECT DETECTED" 🚨</h2>
                    <p style="text-align: center; font-size: 16px; color: #ff00ff;">A person has been identified by the Trinetra .</p>
                    <hr style="border: 1px solid #6600cc;">
                    <p><strong style="color: #00e6e6; font-size:20px;">Name:</strong> <span style="font-size: 20px;color:#ff00ff;">{name}</span></p>
                    <p><strong style="color: #00e6e6; font-size:20px;">Time:</strong> <span style="font-size: 20px;color:#ff00ff;">{timestamp}</span></p>
                    <p><strong style="color: #00e6e6; font-size:20px;">Camera:</strong> <span style="font-size:20px;color:#ff00ff;">{cam_number}</span></p>
                    <p><strong style="color: #00e6e6; font-size:20px;">Location:</strong> <span style="font-size:20px;color:#ff00ff;">{location_str}</span></p>
                    <hr style="border: 1px solid #6600cc;">
                    <div style="text-align: center; margin-top: 15px;">
                        <img src="cid:recognized_face" alt="Recognized Face" style="width: 100%; max-width: 300px; border-radius: 5px; box-shadow: 0px 0px 10px rgba(255, 0, 255, 0.7);">
                    </div>
                    <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #ff66ff;">This is an automated message from  <strong style="color: #00e6e6;">Trinetra</strong>.</p>
                </div>
            </body>
            </html>
            """

            msg = MIMEMultipart()
            msg['From'] = "trinetrasys@gmail.com"
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            # Embed Recognized Face Image
            with open(recognized_image_path, "rb") as face_attachment:
                face_part = MIMEBase('image', 'jpeg')
                face_part.set_payload(face_attachment.read())
                encoders.encode_base64(face_part)
                face_part.add_header('Content-Disposition', 'inline', filename="recognized_face.jpg")
                face_part.add_header('Content-ID', '<recognized_face>')  # This allows embedding
                msg.attach(face_part)

            # Attach footer GIF
            with open("footergi.gif", "rb") as gif_attachment:
                gif_part = MIMEBase('image', 'gif')
                gif_part.set_payload(gif_attachment.read())
                encoders.encode_base64(gif_part)
                gif_part.add_header('Content-Disposition', 'inline', filename="footergi.gif")
                gif_part.add_header('Content-ID', '<footer_gif>')  # This allows embedding
                msg.attach(gif_part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("soooraj2003kerala@gmail.com", "frmycrmgioijdqut")
            server.sendmail("soooraj2003kerala@gmail.com", recipient, msg.as_string())
            server.quit()

        except Exception as e:
            print("Email sending failed:", str(e))

    threading.Thread(target=process_faces, daemon=True).start()
    update_camera_feed()
    root.mainloop()

    for cam in cameras:
        cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    img = sys.argv[1]  # Receives the value of true_img
    r = sys.argv[2]  # Receives the value of recipient_email
    n = sys.argv[3]# Receives the value of recipient_email
    main(r, img, n)
    main(r, img)