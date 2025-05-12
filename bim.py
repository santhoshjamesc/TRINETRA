import os
import cv2

# Load the pre-trained Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
    else:
        os.makedirs(folder_path)

def get_best_picture(folder_path):
    best_image = None
    best_score = 0
    best_face = None

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        # Check for valid image formats
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image = cv2.imread(file_path)

            if image is not None:
                height, width = image.shape[:2]
                resolution = width * height

                # Detect faces
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

                # Score based on face count and resolution
                face_count = len(faces)

                # Check if any faces are detected
                if face_count > 0:
                    center_x, center_y = width // 2, height // 2
                    closest_face = min(
                        faces, key=lambda f: (f[0] + f[2] // 2 - center_x) ** 2 + (f[1] + f[3] // 2 - center_y) ** 2
                    )

                    x, y, w, h = closest_face
                    face_crop = image[y:y+h, x:x+w]

                    # Higher score = more faces + higher resolution + closer to center
                    closest_face_distance = (x + w // 2 - center_x) ** 2 + (y + h // 2 - center_y) ** 2
                    score = face_count * 1000 + resolution - closest_face_distance
                else:
                    # If no faces, just use resolution
                    score = resolution

                # Update best image if a higher score is found
                if score > best_score:
                    best_image = file_path
                    best_score = score
                    best_face = face_crop if face_count > 0 else image

    return best_image, best_face

def main():
    dataset_path = 'dataset'
    persons_folder = 'persons'

    # Ensure dataset folder exists
    if not os.path.exists(dataset_path):
        print(f"Error: '{dataset_path}' folder not found.")
        return

    # Clear the persons folder
    clear_folder(persons_folder)

    # Loop through each subfolder and select the best image
    for subfolder in os.listdir(dataset_path):
        subfolder_path = os.path.join(dataset_path, subfolder)

        if os.path.isdir(subfolder_path):
            best_image, best_face = get_best_picture(subfolder_path)

            if best_image and best_face is not None:
                print(f"Best image in '{subfolder}': {best_image}")

                # Save the cropped face in the persons folder
                image_name = f"{subfolder}.png"
                output_path = os.path.join(persons_folder, image_name)
                cv2.imwrite(output_path, best_face)
            else:
                print(f"No valid images found in '{subfolder}'.")

if __name__ == "__main__":
    main()
