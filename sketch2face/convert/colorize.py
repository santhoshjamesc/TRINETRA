import numpy as np
import argparse
import cv2
import os

# Paths to load the model
PROTOTXT = r"model/colorization_deploy_v2.prototxt"
POINTS = r"model/pts_in_hull.npy"
MODEL = r"model/colorization_release_v2.caffemodel"

# Check if model files exist
if not os.path.isfile(PROTOTXT):
    print("Prototxt file not found:", PROTOTXT)
    exit(1)
if not os.path.isfile(POINTS):
    print("Points file not found:", POINTS)
    exit(1)
if not os.path.isfile(MODEL):
    print("Model file not found:", MODEL)
    exit(1)

# Argparser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
                help="path to input black and white image")
args = vars(ap.parse_args())

# Load the input image
print("Loading input image from path:", args["image"])
image = cv2.imread(args["image"])
if image is None:
    print("Failed to load input image:", args["image"])
    exit(1)
print("Input image loaded successfully with shape:", image.shape)

# Load the Model
print("Loading model...")
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
pts = np.load(POINTS)
print("Model loaded successfully.")

# Load centers for ab channel quantization used for rebalancing
print("Setting up model layers for colorization...")
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
print("Model layers set up successfully.")

# Preprocess the image
print("Preprocessing the input image...")
scaled = image.astype("float32") / 255.0
lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
print("Converted image to LAB color space.")

resized = cv2.resize(lab, (224, 224))
L = cv2.split(resized)[0]
L -= 50
print("Image resized to 224x224 and L channel extracted.")

# Colorizing the image
print("Colorizing the image...")
net.setInput(cv2.dnn.blobFromImage(L))
ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
print("Forward pass through the model completed.")

# Resize the ab channel to match the original image size
ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
print("Resized ab channel to original image dimensions.")

# Combine L and ab channels
L = cv2.split(lab)[0]
colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
print("Combined L and ab channels.")

# Convert LAB to BGR color space
colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
colorized = np.clip(colorized, 0, 1)
print("Converted LAB image back to BGR color space.")

# Scale to 0-255 and convert to uint8
colorized = (255 * colorized).astype("uint8")
print("Scaled colorized image to 0-255 range.")

# Resize images for display
standard_size = (1000, 800)  # Updated standard display size with increased length
original_resized = cv2.resize(image, standard_size)
colorized_resized = cv2.resize(colorized, standard_size)
print(f"Resized images to standard size: {standard_size}")

# Display the original and colorized images
cv2.imshow("Original", original_resized)
cv2.imshow("Colorized", colorized_resized)
print("Displayed the original and colorized images.")

# Ensure "faces" directory exists
output_dir = "faces"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "colorized_output.jpg")

# Save the colorized image without overwriting
counter = 1
while os.path.exists(output_path):
    output_path = os.path.join(output_dir, f"colorized_output_{counter}.jpg")
    counter += 1

cv2.imwrite(output_path, colorized)
print(f"Colorized image saved to {output_path}")

cv2.waitKey(0)
cv2.destroyAllWindows()
print("Program execution completed.")
