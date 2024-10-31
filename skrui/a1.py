from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, array_to_img, load_img
import numpy as np
import os

def augment_brightness_contrast(image_path, output_folder, brightness_range=(0.5, 1.5), contrast_factor=1.2, num_variations=5):
    # Load the image from the specified path. This will be the original image we want to augment.
    image = load_img(image_path)
    
    # Convert the loaded image into a NumPy array format. This is necessary for processing with Keras.
    image_array = img_to_array(image)
    
    # Expand the dimensions of the array to add a batch dimension.
    # Keras expects the input to have a shape of (batch_size, height, width, channels).
    image_array = np.expand_dims(image_array, axis=0)
    
    # Ensure the output folder exists; if it doesn't, create it.
    # This prevents errors when trying to save images to a non-existent directory.
    os.makedirs(output_folder, exist_ok=True)

    # Initialize the ImageDataGenerator with the specified brightness range.
    # This generator will allow us to create augmented images by varying the brightness.
    datagen = ImageDataGenerator(brightness_range=brightness_range)

    # Use the datagen.flow method to generate augmented images in batches.
    # Since we are passing a single image, we will generate multiple variations of it.
    for i, batch in enumerate(datagen.flow(image_array, batch_size=1)):
        # Each 'batch' is a 4D array with the shape (1, height, width, channels).
        # Convert the first image in the batch (the only one in this case) to a PIL Image.
        img = array_to_img(batch[0])
        
        # Convert the PIL Image back into a NumPy array for manipulation.
        img = np.array(img)

        # Apply contrast adjustment by scaling pixel values by the contrast_factor.
        # We use np.clip to ensure that the pixel values remain within the valid range [0, 255].
        # The contrast_factor should be greater than 1 to increase contrast and less than 1 to decrease it.
        img = np.clip(img * contrast_factor, 0, 255).astype(np.uint8)

        # Generate the output file path for saving the augmented image.
        # The naming convention includes a number to distinguish different variations.
        output_path = os.path.join(output_folder, f"variation_{i + 1}.jpg")
        
        # Convert the modified NumPy array back to a PIL Image and save it to the specified output path.
        array_to_img(img).save(output_path)
        
        # Print a message indicating the image has been saved successfully.
        print(f"Saved: {output_path}")

        # Stop generating new images once the specified number of variations is reached.
        # This avoids unnecessary processing after we've created the desired amount of images.
        if i + 1 >= num_variations:
            break

# Parameters
image_path = "avtar.png"  # Replace this with the path to your input image
output_folder = "output_variations"  # Specify the folder where the output images will be saved
brightness_range = (0.5, 1.7)  # Set the range for brightness adjustment; values <1 darken and >1 brighten the image
contrast_factor = 1.4  # Set the contrast multiplier; values >1 increase contrast, <1 decrease contrast
num_variations = 6  # Specify how many variations of the image to generate

# Run the function to create variations of the image using the specified parameters.
augment_brightness_contrast(image_path, output_folder, brightness_range, contrast_factor, num_variations)