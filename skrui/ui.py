import os
import random
import numpy as np
import cv2
from PIL import Image, ImageEnhance
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, array_to_img
import tkinter as tk  # Correctly import tkinter as tk
from tkinter import Label, StringVar, filedialog
from tkinter import ttk  # Correctly import ttk
import winsound  # For sound effect (Windows only
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import time
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, array_to_img, load_img
import numpy as np
import os
from PIL import Image, ImageEnhance
import random
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import cv2
import tkinter as tk
from PIL import Image, ImageTk
progress_bar = None
gpath = ""
uploaded_image_path = None
image_label = None




def process_images(image_path, output_folder, brightness_range=(0.8, 1.2), contrast_range=(0.9, 1.2), 
                  saturation_range=(0.9, 1.1), max_perspective_warp=0.05, num_variations=100):
    """Processes an image to generate various augmented variations."""
    
    def random_perspective(img, max_warp=0.05):
        """Applies a subtle perspective transformation to the image."""
        width, height = img.size
        
        # Define the distortion limits for each corner of the image with a reduced warp effect
        dx = width * max_warp
        dy = height * max_warp
        
        # Randomly shift each corner within the defined limits for a subtle effect
        x0, y0 = random.uniform(-dx, dx), random.uniform(-dy, dy)
        x1, y1 = width + random.uniform(-dx, dx), random.uniform(-dy, dy)
        x2, y2 = width + random.uniform(-dx, dx), height + random.uniform(-dy, dy)
        x3, y3 = random.uniform(-dx, dx), height + random.uniform(-dy, dy)
        
        # Define the original and transformed coordinates
        original_coords = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
        transformed_coords = np.float32([[x0, y0], [x1, y1], [x2, y2], [x3, y3]])
        
        # Calculate the perspective transformation matrix
        matrix = cv2.getPerspectiveTransform(original_coords, transformed_coords)
        
        # Convert the PIL image to an OpenCV format for transformation
        img_cv = np.array(img)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
        
        # Apply the perspective transformation
        warped_img = cv2.warpPerspective(img_cv, matrix, (width, height))
        
        # Convert back to PIL format
        return Image.fromarray(cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB))

    # Load the original image
    image = load_img(image_path)
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Initialize ImageDataGenerator with general augmentation parameters
    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Setup Tkinter progress window
    # Setup Tkinter progress window
    root = tk.Tk()  # Use tk.Tk() to create the main window
    root.title("Image Augmentation Progress")
    root.geometry("600x150")  # Increased window width

    label = tk.Label(root, text="Generating Images...")
    label.pack(pady=10)

    progress_var = StringVar()
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")  # Use ttk.Progressbar
    progress_bar.pack(pady=10)
    progress_bar["maximum"] = num_variations
    # Generate augmented images
    for i, batch in enumerate(datagen.flow(image_array, batch_size=1)):
        # Convert to PIL image for transformations
        img = array_to_img(batch[0])
        
        # Apply brightness, contrast, and saturation adjustments within a limited range
        current_brightness = random.uniform(brightness_range[0], brightness_range[1])
        current_contrast = random.uniform(contrast_range[0], contrast_range[1])
        current_saturation = random.uniform(saturation_range[0], saturation_range[1])

        img = ImageEnhance.Brightness(img).enhance(current_brightness)
        img = ImageEnhance.Contrast(img).enhance(current_contrast)
        img = ImageEnhance.Color(img).enhance(current_saturation)
        
        # Randomly apply perspective transformation only if subtle effect is needed
        if random.choice([True, False]):
            img = random_perspective(img, max_perspective_warp)
        
 # Save the augmented image
        # Update progress bar and label
        progress_bar["value"] = i + 1
        label.config(text=f"Saved image {i + 1} of {num_variations}")
        root.update_idletasks()
        output_path = os.path.join(output_folder, f"{i + 1}.jpg")
        opath = os.path.join(output_folder)
        img.save(output_path)
        print(f"Saved: {output_path}")
        
        global gpath
        gpath = os.path.abspath(opath)
        
        # Stop after generating the specified number of variations
        if i + 1 >= num_variations:
            break
    
    # Play a sound effect when the progress reaches 100%
    winsound.Beep(2500, 1000)  # 2500 Hz frequency, 1000 ms duration
    
    label.config(text="All images generated!")
    root.update_idletasks()
    root.destroy()  # Close the progress window

# Function to close the splash screen and open the home screen
def navigate_to_home():
    # Destroys the splash screen window to remove it from view
    splash_screen.destroy()
    # Calls the function to initialize and display the main home screen
    show_home_screen()

# Function to simulate a loading progress bar on the splash screen
def run_loader():
    # Set the progress bar's initial value to 0 (empty)
    progress['value'] = 0
    # Define the maximum value for the progress bar (i.e., fully loaded state)
    max_value = 100

    # Loop from 0 to the maximum value, incrementally filling the progress bar
    for i in range(max_value + 1):
        time.sleep(0.015)  # Wait 15ms for each step, making the entire loading time around 1.5 seconds
        progress['value'] = i  # Set the current value of the progress bar to the current step in the loop
        splash_screen.update_idletasks()  # Refresh the splash screen to visually update the progress


def start_surveillance():
    global uploaded_image_path, left_frame, image_label  # Ensure we can access the uploaded image path
    # Clear the home screen content
    for widget in home_screen.winfo_children():
        widget.destroy()

    # Initialize video captures for four cameras
    cap0 = cv2.VideoCapture(0)
    cap1 = cv2.VideoCapture(1)
    cap2 = cv2.VideoCapture(2)
    cap3 = cv2.VideoCapture(3)

    # Create a main frame to hold left and right sections
    main_frame = tk.Frame(home_screen, bg="#1e1e1e")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Left frame for buttons or controls
    left_frame = tk.Frame(main_frame, bg="#1e1e1e", width=200)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

    # Right frame for the video feed
    right_frame = tk.Frame(main_frame, bg="#1e1e1e")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
    right_frame.pack_propagate(False)

    # Add a "Back to Home" button in the left frame
    back_button = tk.Button(left_frame, text="Back to Home", command=lambda: back_to_home(cap0, cap1, cap2, cap3), font=("Arial", 12), bg="#e74c3c", fg="white")
    back_button.pack(pady=10, padx=20)

    # Entry field for the image name
    global name_entry  # Declare name_entry as global to access it
    name_entry = tk.Entry(left_frame, font=("Arial", 12))
    name_entry.pack(pady=(10, 5))  # Add padding for spacing

    # Display the uploaded image in the left frame
    if uploaded_image_path is not None:
        display_image(uploaded_image_path)

    # Label to display the combined video feed in the right frame
    video_label = tk.Label(right_frame)
    video_label.pack(fill=tk.BOTH, expand=True)

    def update_frame():
        # Capture frames from each camera
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()

        # Check if frames were captured successfully
        if ret0 and ret1 and ret2 and ret3:
            # Stack frames in a 2x2 grid
            top_row = cv2.hconcat([frame0, frame1])
            bottom_row = cv2.hconcat([frame2, frame3])
            combined_frame = cv2.vconcat([top_row, bottom_row])

            # Convert the combined frame to RGB for Tkinter display
            combined_frame = cv2.cvtColor(combined_frame, cv2.COLOR_BGR2RGB)

            # Convert to ImageTk format
            img = Image.fromarray(combined_frame)
            img_tk = ImageTk.PhotoImage(image=img)

            # Update the label with the new image
            video_label.img_tk = img_tk  # Keep a reference to avoid garbage collection
            video_label.configure(image=img_tk)

        # Repeat the update every 33 ms (approx. 30 FPS)
        home_screen.after(33, update_frame)

    # Start the video feed
    update_frame()


def back_to_home(*caps):
    # Release all video captures
    for cap in caps:
        cap.release()
    # Clear the home screen and reload the home content
    load_home_content(None)

def show_home_screen():
    # Declare home_screen as a global variable so it can be accessed in other functions
    global home_screen, logo_image  # Include logo_image to be reused
    # Initialize the main application window and set the title
    home_screen = tk.Tk()
    home_screen.title("Trinetra - 'More than Meets the Eye'")  # Application title for the home screen

    # Set the home screen window to cover the full screen resolution of the user's display
    home_screen.geometry(f"{home_screen.winfo_screenwidth()}x{home_screen.winfo_screenheight()}")
    # Configure the background color of the home screen window to dark gray
    home_screen.configure(bg='#1e1e1e')

    # Load and display the application's logo image on the home screen
    # Replace "trinetra.png" with the correct path for the logo image file
    logo_image = tk.PhotoImage(file="trinetra.png")  
    home_screen.iconphoto(False, logo_image)  # Set the logo image as the window's icon

    # Call a function to populate the home screen's content (buttons, labels, etc.)
    load_home_content(logo_image)
    # Start the main event loop for the home screen to wait for user actions
    home_screen.mainloop()

# Function to display the content (logo, welcome message, buttons) on the home screen
def load_home_content(logo_image):
    # Clear all widgets in the home screen window to prepare for new content
    for widget in home_screen.winfo_children():
        widget.destroy()

    # Display the application's logo at the top of the home screen
    logo_label = tk.Label(home_screen, image=logo_image, bg='#1e1e1e')
    logo_label.pack(pady=(2, 2))  # Add vertical padding above and below the logo

    # Display a welcome message for the user below the logo
    home_label = tk.Label(home_screen, text="Welcome Home User!", font=("Arial", 15), bg='#1e1e1e', fg='white')
    home_label.pack(pady=(1, 3))

    # Description of available features, with each feature listed on a new line
    description_label = tk.Label(
        home_screen, 
        text="1. Face Sketch:\nCreates a digital sketch using facial features for identification.\n\n"
             "2. Surveillance:\nUpload a photo, track individuals through surveillance cameras.\n"
             "Alerts authorities with location if detected.",
        font=("Arial", 12), 
        bg='lightgrey', 
        fg='black', 
        anchor="w", 
        justify="left"
    )
    # Pack description label with padding for spacing from the edges of the window
    description_label.pack(padx=30, pady=30)

    # Create a frame to hold the main feature buttons horizontally
    button_frame = tk.Frame(home_screen, bg='#1e1e1e')
    button_frame.pack(pady=30)  # Add vertical padding to separate buttons from other elements

    # Button for "Face Sketch" feature
    button1 = tk.Button(button_frame, text=" FACE SKETCH ", command=lambda: button_action(1), font="Arial 15 bold", padx=10, bg="#f7a014",
                        fg="white", pady=5, bd=10, highlightthickness=0, activebackground="#091428",
                        activeforeground="#1e1e1e")
    button1.pack(side=tk.LEFT, padx=(20, 38), anchor='w')  # Position button on the left, with padding between buttons

    # Button for "Surveillance" feature
    # Directly call start_surveillance when the button is clicked
    button2 = tk.Button(button_frame, text=" SURVEILLANCE  ", command=start_surveillance, font="Arial 15 bold", padx=20, bg="#f7a014",
                        fg="white", pady=5, bd=10, highlightthickness=0, activebackground="#091428",
                        activeforeground="#1e1e1e")
    button2.pack(side=tk.LEFT, padx=(38, 20), anchor='e')
    # Button for "Generate Dataset" feature, triggers screen change to dataset generation options
    button3 = tk.Button(button_frame, text=" GENERATE DATASET  ", command=show_generate_dataset_screen, font="Arial 15 bold", padx=20, bg="#f7a014",
                        fg="white", pady=5, bd=10, highlightthickness=0, activebackground="#091428",
                        activeforeground="#1e1e1e")
    button3.pack(side=tk.LEFT, padx=(38, 20), anchor='e')  # Position button on the far right with padding

# Function to display the Generate Dataset screen within the same home screen window
# Function to display the Generate Dataset screen within the same home screen window


# Global variable for storing uploaded image path and name
uploaded_image_path = None  # Initialize at a higher scope
image_name = None  # To store the user-defined name for the image
# Declare left_frame as a global variable
global left_frame

# Declare right_frame as a global variable
global right_frame



def show_generate_dataset_screen():
    global left_frame, right_frame  # Declare both left_frame and right_frame as global

    # Clear all widgets from the home screen to prepare for the Generate Dataset screen
    for widget in home_screen.winfo_children():
        widget.destroy()

    # Create a main frame to hold the left and right sections
    main_frame = tk.Frame(home_screen, bg='#1e1e1e')
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a left frame for the uploaded image and buttons with a border
    left_frame = tk.Frame(main_frame, bg='#1e1e1e', width=300, bd=2, relief=tk.SUNKEN)  # Added bd and relief
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5), pady=10)

    # Create a right frame for the generated images
    right_frame = tk.Frame(main_frame, bg='#1e1e1e')
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)

    # Button to navigate back to the home screen content without closing the window
    back_button = tk.Button(left_frame, text="Back to Home", command=lambda: load_home_content(None), font=("Arial", 12), bg="#e74c3c", fg="white")
    back_button.pack(pady=(10, 10))  # Add padding to space the back button from other elements

    # Display a title for the Generate Dataset screen
    title_label = tk.Label(left_frame, text="Generate Dataset", font=("Arial", 18, "bold"), fg="white", bg='#1e1e1e')
    title_label.pack(pady=(10, 5))  # Add padding to space the title from other elements

    # Provide instructions for uploading an image to generate a dataset
    instruction_label = tk.Label(left_frame, text="Please upload an image to generate a dataset.", font=("Arial", 12), fg="white", bg='#1e1e1e')
    instruction_label.pack(pady=(5, 20))  # Add padding to space the instructions from other elements

    # Label for the entry field
    name_label = tk.Label(left_frame, text="Enter Image Name:", font=("Arial", 12), fg="white", bg='#1e1e1e')
    name_label.pack(pady=(20, 5))  # Increased top padding

    # Entry widget for the user to input the image name
    global name_entry
    name_entry = tk.Entry(left_frame, font=("Arial", 12))  # Create an entry field for the image name
    name_entry.pack(pady=(10, 5))  # Add padding for spacing

    # Bind key release event to the function
    name_entry.bind("<KeyRelease>", on_name_entry_change)  # Bind key release event to the function

    # Button to trigger the image upload process
    upload_button = tk.Button(left_frame, text="Upload Image", command=upload_image, font=("Arial", 12), bg="#3e8e41", fg="white")
    upload_button.pack(pady=(20, 10))  # Increased top padding

    # Initialize the run button and image label as None, to be created only when needed
    global run_button, image_label
    run_button = None  # Initially no run button present
    image_label = None  # Initially no image label present




def display_generated_images(output_folder):
    global right_frame  # Access the right_frame variable

    # Clear any existing images or widgets in the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Display a title for the generated images
    title_label = tk.Label(right_frame, text="Generated Images", font=("Arial", 18, "bold"), fg="white", bg='#1e1e1e')
    title_label.pack(pady=10)

    # Create a canvas for the generated images in the right frame
    canvas = tk.Canvas(right_frame, bg='#1e1e1e')
    scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')

    # Update the canvas scroll region whenever the size of scrollable_frame changes
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Place the scrollable frame inside the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the canvas and scrollbar in the right frame
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Display the generated images in a grid layout in the scrollable frame
    columns = 6  # Set the number of columns in the grid
    row, col = 0, 0  # Initialize row and column counters

    for file in os.listdir(output_folder):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            img_path = os.path.join(output_folder, file)
            img = Image.open(img_path)
            img = img.resize((220, 220), Image.LANCZOS)  # Resize to a consistent size
            img = ImageTk.PhotoImage(img)  # Convert the PIL image to a format suitable for Tkinter

            # Create a label to hold and display the generated image
            image_label = tk.Label(scrollable_frame, image=img, bg='#1e1e1e')
            image_label.grid(row=row, column=col, padx=15, pady=15)  # Use grid layout for positioning

            # Keep a reference to avoid garbage collection
            image_label.image = img

            # Update row and column counters to arrange images in a grid
            col += 1
            if col >= columns:  # Move to the next row after reaching the column limit
                col = 0
                row += 1



def upload_image():
    global uploaded_image_path  # Use the global variable to track the uploaded image
    # Open file dialog to allow the user to select an image file from their computer
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
    if file_path:  # If a file was selected (not canceled)
        uploaded_image_path = file_path  # Store the uploaded image path
        print(f"Image uploaded: {uploaded_image_path}")  # Print file path for confirmation

        # Display the uploaded image on the Generate Dataset screen
        display_image(file_path)

        # If this is the first image upload, display a "Run" button below the image
        global run_button
        if run_button is None:  # Ensure run button is only added once
            run_button = tk.Button(
                left_frame,  # Changed to left_frame to position it correctly
                text="Run", 
                font=("Arial", 12), 
                command=process_image,  # Function to be called on button click
                bg="#5b9bd5", 
                fg="white",
                state=tk.DISABLED  # Initially disabled
            )
            run_button.pack(pady=10)  # Position the "Run" button with padding below the uploaded image


def display_image(file_path):
    global image_label, img, left_frame  # Access the left_frame variable
    # Open the selected image file and resize it for display within the application window
    img = Image.open(file_path)
    img = img.resize((250, 300), Image.LANCZOS)  # Resize to a larger size for display
    img = ImageTk.PhotoImage(img)  # Convert the PIL image to a format suitable for Tkinter

    # Check if image_label exists (image already displayed) and update it, or create it if not
    if image_label is None:
        # Create a new label to hold and display the uploaded image
        image_label = tk.Label(left_frame, image=img, bg='#1e1e1e')
        image_label.pack(pady=10)  # Add padding below the image for spacing
    else:
        # Update the existing label to show the new uploaded image
        image_label.configure(image=img)  # Change the displayed image to the newly uploaded image

    # Keep a reference to avoid garbage collection
    image_label.image = img

def on_name_entry_change(event):
    """Enable the run button if the entry is not empty, disable it if it is."""
    if name_entry.get().strip():  # Check if the entry has text
        run_button.config(state=tk.NORMAL)  # Enable the run button
    else:
        run_button.config(state=tk.DISABLED)  # Disable the run button

def process_image():
    """Placeholder function to simulate processing of the uploaded image."""
    image_name = name_entry.get().strip()  # Get the user-defined name for the image
    # Here you would call the function that processes the image using the provided name
    print(f"Processing image: {uploaded_image_path} with name: {image_name}")
    brightness_range = (0.5, 1.2)  # Reduced brightness range
    contrast_range = (0.5, 1.5)  # Slight contrast adjustment range
    saturation_range = (0.3, 1.4)  # Very slight saturation adjustment range
    max_perspective_warp = 0.05  # Very small perspective distortion factor (5%)
    print(f"Uploaded Image Path: {uploaded_image_path}")
    print(f"Image Name: {image_name}")

    process_images(uploaded_image_path, image_name, brightness_range, contrast_range, saturation_range, max_perspective_warp, 50)
    
    display_generated_images(gpath)

 
# Create and configure the splash screen window
splash_screen = tk.Tk()
splash_screen.title("Splash Screen")  # Title for the splash screen
splash_screen.geometry("800x700")  # Set splash screen dimensions for appearance
splash_screen.overrideredirect(True)  # Remove window decorations (e.g., title bar) for a cleaner look

# Center the splash screen on the user's display
screen_width = splash_screen.winfo_screenwidth()
screen_height = splash_screen.winfo_screenheight()
x = (screen_width // 2) - (800 // 2)  # Calculate x position to center horizontally
y = (screen_height // 2) - (700 // 2)  # Calculate y position to center vertically
splash_screen.geometry(f"800x700+{x}+{y}")  # Set the geometry of the splash screen with calculated position

# Set background color of the splash screen and load the application logo
splash_screen.configure(bg='#1e1e1e')  # Dark gray background for splash screen
logo_image = tk.PhotoImage(file="trinetra.png")  # Load the logo image
splash_screen.iconphoto(False, logo_image)  # Set the logo image as the window's icon

# Add widgets to the splash screen: logo, brand name, slogan, and progress bar
logo_label = tk.Label(splash_screen, image=logo_image, bg='#1e1e1e')
logo_label.pack(pady=10)  # Add vertical padding for the logo
brand_name_label = tk.Label(splash_screen, text="TRINETRA", font=("Arial", 20, "bold"), fg="white", bg='#1e1e1e')
brand_name_label.pack()  # Display the brand name
slogan_label = tk.Label(splash_screen, text="More Than Meets the Eye", font=("Arial", 12, "italic"), fg="white", bg='#1e1e1e')
slogan_label.pack(pady=5)  # Display the slogan with some padding

# Configure and display a progress bar to indicate loading progress
progress = ttk.Progressbar(splash_screen, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress.pack(pady=20)  # Add padding for spacing

# Start the loading animation and transition to the home screen after a delay
splash_screen.after(100, run_loader)  # Start the loader after a short delay
splash_screen.after(3500, navigate_to_home)  # Navigate to home after 3.5 seconds

# Display the splash screen and begin the application's main event loop
splash_screen.mainloop()
