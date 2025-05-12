import os
import random
import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk, StringVar
from tensorflow.keras.preprocessing.image import load_img, img_to_array, array_to_img, ImageDataGenerator
from PIL import Image, ImageEnhance
import bim

def process_images(totaln, image_path, output_folder, brightness_range=(0.8, 1.2), contrast_range=(0.9, 1.2),
                  saturation_range=(0.9, 1.1), max_perspective_warp=0.05, num_variations=6):
    """Processes an image to generate various augmented variations."""

    def random_perspective(img, max_warp=0.05):
        """Applies a subtle perspective transformation to the image."""
        width, height = img.size

        dx = width * max_warp
        dy = height * max_warp

        x0, y0 = random.uniform(-dx, dx), random.uniform(-dy, dy)
        x1, y1 = width + random.uniform(-dx, dx), random.uniform(-dy, dy)
        x2, y2 = width + random.uniform(-dx, dx), height + random.uniform(-dy, dy)
        x3, y3 = random.uniform(-dx, dx), height + random.uniform(-dy, dy)

        original_coords = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
        transformed_coords = np.float32([[x0, y0], [x1, y1], [x2, y2], [x3, y3]])

        matrix = cv2.getPerspectiveTransform(original_coords, transformed_coords)

        img_cv = np.array(img)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

        warped_img = cv2.warpPerspective(img_cv, matrix, (width, height))

        return Image.fromarray(cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB))

    try:
        image = load_img(image_path)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Save the original image
    os.makedirs(output_folder, exist_ok=True)
    original_path = os.path.join(output_folder, f"{totaln}.jpg")
    image.save(original_path)
    print(f"Saved original image: {original_path}")

    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)

    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    root = tk.Tk()
    root.title("Image Augmentation Progress")
    root.geometry("600x150")

    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 600) // 2
    y = (screen_height - 150) // 2
    root.geometry(f"600x150+{x}+{y}")

    root.configure(bg="#120e26")

    label = tk.Label(root, text="Generating Images...", fg="#0ff", bg="#120e26", font=("Courier New", 14, "bold"))
    label.pack(pady=10)

    progress_var = StringVar()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Cyberpunk.Horizontal.TProgressbar", troughcolor="#222", background="#0ff", thickness=10)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", style="Cyberpunk.Horizontal.TProgressbar")
    progress_bar.pack(pady=20)
    progress_bar["maximum"] = num_variations

    for i, batch in enumerate(datagen.flow(image_array, batch_size=1)):
        img = array_to_img(batch[0])

        try:
            current_brightness = random.uniform(brightness_range[0], brightness_range[1])
            current_contrast = random.uniform(contrast_range[0], contrast_range[1])
            current_saturation = random.uniform(saturation_range[0], saturation_range[1])

            img = ImageEnhance.Brightness(img).enhance(current_brightness)
            img = ImageEnhance.Contrast(img).enhance(current_contrast)
            img = ImageEnhance.Color(img).enhance(current_saturation)

            if random.choice([True, False]):
                img = random_perspective(img, max_perspective_warp)

            progress_bar["value"] = i + 1
            label.config(text=f"Saved image {i + 1} of {num_variations}")
            root.update_idletasks()

            output_path = os.path.join(output_folder, f"{totaln + i + 1}.jpg")
            img.save(output_path)
            print(f"Saved: {output_path}")

        except Exception as e:
            print(f"Error processing image {i + 1}: {e}")

        if i + 1 >= num_variations:
            break

    label.config(text="All images generated!")
    root.update_idletasks()
           
    bim.main()  # Execute bim.main() during loading phase
  # Wait for bim.main() to finish before training starts


    root.quit()
    root.destroy()

# Example usage (uncomment and set appropriate paths)
# process_images(totaln=0, image_path='path/to/image.jpg', output_folder='path/to/output/folder')
