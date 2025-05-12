import os
import random
import numpy as np
import cv2
import time
import logging
import json
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pygame
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, array_to_img
from tkinter import Tk, Button, Label, Frame, Canvas
from PIL import Image, ImageTk
from tkinter import ttk, StringVar
import tkinter as tk
from tkinter import Label, StringVar, filedialog, ttk, messagebox, PhotoImage
from PIL import Image, ImageEnhance, ImageTk
from playsound import playsound
from tkinter import Toplevel
from tkinter import font
from tkinter import Tk, Frame, BOTH, Label
from tkinter import filedialog
# Import your configuration settings



# Global variables
progress_bar = None
gpath = ""
uploaded_image_path = None
image_label = None
uploaded_image_paths = []
current_index = 0
run_button = None
next_button = None
previous_button = None
folder_info_text = None
train_button = None
left_frame = None
right_frame = None
login_screen = None
home_screen = None
splash_screen = None
logo_image = None
name_entry = None
totaln=0
user_id= None

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


import warnings
warnings.filterwarnings('ignore', category=UserWarning)
from datasetgen import process_images


CASCADE_FILE = "haarcascade_frontalface_default.xml"
PROFILE_CASCADE_FILE = "haarcascade_profileface.xml"

# Load cascade classifiers
frontal_detector = cv2.CascadeClassifier(CASCADE_FILE)
profile_detector = cv2.CascadeClassifier(PROFILE_CASCADE_FILE)

if frontal_detector.empty() or profile_detector.empty():
    raise ValueError("Error loading cascade classifiers")



PATHS = {
    
    'cascade_file': 'haarcascade_frontalface_default.xml',
    'profile_cascade_file': 'haarcascade_profileface.xml',
    'names_file': 'names.json',
}

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------------------------------------------- DATASET GENERATION------------------------------
def show_cyberpunk_warning(message):
    cyber_window = tk.Toplevel()
    cyber_window.title("Warning")
    cyber_window.geometry("600x170")
    cyber_window.configure(bg="#120e26")

    # Center the warning window on the screen without root
    screen_width = cyber_window.winfo_screenwidth()
    screen_height = cyber_window.winfo_screenheight()
    window_width = 600
    window_height = 170
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    cyber_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    frame = tk.Frame(cyber_window, bg="#120e26", bd=2)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    label = tk.Label(frame, text=message, fg="#0ff0fc", bg="#120e26", font=("Courier New", 12, "bold"))
    label.pack(pady=10)

    button = tk.Button(frame, text="OK", command=cyber_window.destroy, bg="#ff00ff", fg="#000", font=("Courier New", 12, "bold"), relief="flat")
    button.pack(pady=5)



def process_image():
    image_name = name_entry.get().strip()
    if not image_name:
        show_cyberpunk_warning("Input Required:Enter a name before running the process.")
        return
    totaln = 0
    dataset_folder = os.path.join(os.getcwd(), "dataset")
    os.makedirs(dataset_folder, exist_ok=True)
    output_folder = os.path.join(dataset_folder, image_name)
    os.makedirs(output_folder, exist_ok=True)

    for uploaded_image_path in uploaded_image_paths:
        print("processing..............", uploaded_image_path, "........ no==", totaln)
        print(f"Processing image: {uploaded_image_path} with name: {image_name}")
        brightness_range = (0.5, 1.2)
        contrast_range = (0.5, 1.5)
        saturation_range = (0.3, 1.4)
        max_perspective_warp = 0.05
        print(f"Uploaded Image Path: {uploaded_image_path}")
        print(f"Image Name: {image_name}")

        process_images(totaln, uploaded_image_path, output_folder, brightness_range, contrast_range, saturation_range, max_perspective_warp, 10)
    
        totaln += 10

    print("Image transfer to dataset folder complete!")
    # pygame.mixer.init()
    # pygame.mixer.music.load("./assets/pkkr.wav")
    # pygame.mixer.music.play()
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)
    display_generated_images(output_folder)

def show_generate_dataset_screen():
    global left_frame, right_frame, name_entry, uploaded_image_paths, current_index, image_label, run_button, next_button, previous_button


    
    # Reset global variables
    uploaded_image_paths = []
    current_index = 0
    image_label = None
    run_button = None
    next_button = None
    previous_button = None
   
    # Clear all widgets from the home screen to prepare for the Generate Dataset screen
    for widget in home_screen.winfo_children():
        widget.destroy()


    main_frame = tk.Frame(home_screen, bg='#0f051d')
    main_frame.pack(fill=tk.BOTH, expand=True)

    main_frame.grid_columnconfigure(0, weight=0)  # Left frame stays its set size
    main_frame.grid_columnconfigure(1, weight=1)  # Right frame expands to fill remaining space

    left_frame = tk.Frame(main_frame, bg='#120e26', bd=2, relief=tk.SUNKEN)
    left_frame.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)

    # Force the width and height
    left_frame.config(width=600, height=800)
    left_frame.grid_propagate(False)  # Stop resizing based on content
    left_frame.update_idletasks()  # Apply the size change

    right_frame = Frame(main_frame, bg='#1e1e1e', width=800, height=600)
    right_frame.grid_propagate(False)  # Prevents resizing based on content
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

    bg_image = Image.open("./assets/dataset.jpg")
    bg_image = bg_image.resize((right_frame.winfo_screenwidth(), right_frame.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(right_frame, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    main_frame.grid_rowconfigure(0, weight=1)
    button_style = {
        'borderwidth': 4,
        'highlightthickness': 0,
        'padx': 10,
        'pady': 5,
        'fg': 'white',
        'font': ("Arial", 14),
        'bg': '#7f00ff',  # Updated button color to match the cyberpunk theme
        'relief': 'flat',
        'activebackground': '#7f00ff',  # Same as bg to avoid color change
        'activeforeground': 'black'    # Same as fg to avoid color change
    }
    back_arrow = "⮐"
    back_button_style = {
        'borderwidth': 4,
        'highlightthickness': 0,
        'padx': 10,  # Increase padding to create rounder shape
        'pady': 10,
        'fg': 'white',
        'font': ('Helvetica', 25, 'bold'),
        'bg': '#7f00ff',
        'relief': 'flat',
        'activebackground': '#7f00ff',  # Same as bg to avoid color change
        'activeforeground': 'black'    # Same as fg to avoid color change
        }

    # Use canvas to make the button rounded
    back_button = tk.Button(left_frame, text=back_arrow, command=back_to_home, **back_button_style)
    back_button.place(x=10, y=10, width=65, height=65)  # Adjust width and height for round look

# Optional: make the button’s corners visually rounder
    back_button.config(highlightbackground='#7f00ff', highlightcolor='#7f00ff')

    title_label = tk.Label(left_frame, text="DATASET GENERATION", font=("Courier New", 30, "bold"), fg="white", bg='#120e26')
    title_label.pack(pady=(100, 5), padx=1)

    instruction_label = tk.Label(left_frame, text="    Upload the image of the Suspect/Missing person    ", font=("Courier New", 20), fg="white", bg='#120e26')
    instruction_label.pack(pady=(10, 10), padx=1)

    name_label = tk.Label(left_frame, text="Enter the name:", font=("Courier New", 17), fg="white", bg='#120e26')
    name_label.pack(pady=(20, 5), padx=1)

    name_entry = tk.Entry(left_frame, font=("Arial", 17), bg='white', fg='black', insertbackground='black')
    name_entry.pack(pady=(10, 5), padx=1)

    upload_button = tk.Button(left_frame, text="UPLOAD IMAGE", command=upload_image, **button_style)
    upload_button.pack(pady=(20, 10), padx=1)


    home_screen.mainloop()
  
def upload_image():
    global uploaded_image_paths, current_index, run_button
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_paths:
        uploaded_image_paths = list(file_paths)
        print(f"Images uploaded: {', '.join(uploaded_image_paths)}")
        display_image(uploaded_image_paths[current_index])
        if run_button is None:
            run_button = tk.Button(left_frame, text="GENERATE", font=("Arial", 17,"bold"), command=process_image, bg="#ff00ff", fg="white", relief=tk.FLAT, borderwidth=0, highlightthickness=0)
            run_button.pack(pady=10)
            run_button.config(height=2, width=29, bd=0, highlightthickness=0)
            run_button.configure(borderwidth=4, highlightbackground='#ff00ff', highlightcolor='#ff00ff', padx=10, pady=5)
            run_button.config(relief=tk.FLAT)

def display_image(file_path):
    print("-------------------------------display------------------------")
    global image_label, img, left_frame, next_button, previous_button  # Access the left_frame variable
    # Open the selected image file and resize it for display within the application window
    img = Image.open(file_path)
    img = img.resize((400, 400), Image.LANCZOS)  # Resize to a larger size for display
    img = ImageTk.PhotoImage(img)  # Convert the PIL image to a format suitable for Tkinter
    button_style = {
        "borderwidth": 4,
        "highlightthickness": 0,
        "padx": 13,
        "pady": 159,
        "fg": "pink",
        "font": ("Arial", 25, "bold"),
        "bg": "#7f00ff",
        "activebackground": "#7f00ff",  # Same as bg to avoid color change
        "activeforeground": "black"    # Same as fg to avoid color change
    }
    
    # Create buttons for Next and Previous actions if they don't already exist
    if next_button is None or previous_button is None:
        next_button = tk.Button(left_frame, text="⯈", command=next_image,**button_style)
        next_button.place(relx=0.88, rely=.42)

        previous_button = tk.Button(left_frame, text="⯇", command=previous_image,**button_style)
        previous_button.place(relx=0.01, rely=.42)
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

def next_image():
    global current_index
    if current_index < len(uploaded_image_paths) - 1:
        current_index += 1
    else:
        current_index = 0  # Loop back to the first image
    display_image(uploaded_image_paths[current_index])  # Display the next image

def previous_image():
    global current_index
    if current_index > 0:
        current_index -= 1
    else:
        current_index = len(uploaded_image_paths) - 1  # Loop back to the last image
    display_image(uploaded_image_paths[current_index])  # Display the previous image

def display_generated_images(output_folder):
    global right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(right_frame, text="GENERATED IMAGE", font=("Courier New", 25, "bold"), fg="white", bg='#1e1e1e')
    title_label.pack(pady=10)

    # Create a frame for the canvas and scrollbar to avoid scrollbar resizing issues
    container = tk.Frame(right_frame, bg='#1e1e1e')
    container.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(container, bg='#1e1e1e')
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    columns = 4
    row, col = 0, 0

    for file in os.listdir(output_folder):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            img_path = os.path.join(output_folder, file)
            img = Image.open(img_path)
            img = img.resize((239, 239), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            image_label = tk.Label(scrollable_frame, image=img, bg='#1e1e1e')
            image_label.grid(row=row, column=col, padx=15, pady=15)

            image_label.image = img

            col += 1
            if col >= columns:
                col = 0
                row += 1

    # Enable mouse wheel scrolling on Windows
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))



def on_name_entry_change(event):
    """Enable the run button if the entry is not empty, disable it if it is."""
    if name_entry.get().strip():  # Check if the entry has text
        run_button.config(state=tk.NORMAL)  # Enable the run button
    else:
        run_button.config(state=tk.DISABLED)  # Disable the run button


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------SURVEILLANCE-------------------------------

import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import shutil
import recogggg1
import shutil
import subprocess


import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import shutil
import recogggg1
import shutil
import subprocess

def image_surveillance():
    global surveillance_button, true_img, image_refs, selected_button, selected_image_label, selected_image_display  # Add selected_image_display to globals

    # Clear the home screen
    for widget in home_screen.winfo_children():
        widget.destroy()

 # Main container frame
    main_frame = tk.Frame(home_screen, bg='#1e1e1e')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Create a frame for the back button
    back_button_frame = tk.Frame(main_frame, bg='#1e1e1e')
    back_button_frame.pack(side=tk.TOP, fill=tk.X)

    # Back button configuration
    back_arrow = "⮐"
    back_button_style = {
        'borderwidth': 4,
        'highlightthickness': 0,
        'padx': 0,
        'pady': 0,
        'fg': 'white',
        'font': ('Helvetica', 25, 'bold'),
        'bg': '#7f00ff',
        'relief': 'flat',
        'activebackground': '#7f00ff',
        'activeforeground': 'black'
    }

    # Create the back button and place it in the back button frame
    back_button = tk.Button(back_button_frame, text=back_arrow, command=back_to_home, **back_button_style)
    back_button.pack(side=tk.LEFT, padx=0, pady=10)

    name_label = tk.Label(text="Select Target:", font=("Courier New", 25,"bold"), fg="white", bg='#120e26')
    name_label.place(x=200, y=35)  # Adjust x and y values as needed for padding

    # Set the desired width, height, and offset for the canvas
    canvas_width = 710  # Set the desired width for the canvas
    canvas_height = 900  # Set the desired height for the canvas
    canvas_offset = 2   # Set the offset from the left side

    # Create a scrollable canvas for images
    canvas = tk.Canvas(main_frame, bg="#1e1e1e", width=canvas_width, height=canvas_height)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the scrollbar on the right side of the canvas
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)  # Do not expand the canvas

    # Use place to set the canvas position with an offset
    canvas.place(x=canvas_offset, y=87)  # Apply the offset

    # Ensure the canvas does not resize with the window
    main_frame.pack_propagate(False)  # Prevent the main frame from resizing to fit its children
    canvas.pack_propagate(False)  # Prevent the canvas from resizing to fit its children

    # Bind mouse wheel events for scrolling
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # For Windows
    canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))  # For Linux
    canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))  # For Linux

    # Ensure the "persons" folder exists
    persons_folder = os.path.join(os.getcwd(), "persons")
    if not os.path.exists(persons_folder):
        messagebox.showerror("Error", f"Folder '{persons_folder}' not found!")
        return

    # Collect image files
    image_files = [f for f in os.listdir(persons_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        messagebox.showinfo("Info", "No images found in 'persons' folder.")
        return

    # Global list to store references to prevent garbage collection
    image_refs = []

    # Create a label to display the selected image name
    selected_image_label = tk.Label(main_frame, text="➜ ", bg="#1e1e1e", fg="white", font=("Courier New",30 , "bold"))
    selected_image_label.pack(pady=(100, 0), padx=(920, 0))  # Add some padding above the label

    # Create a label to display the selected image
    selected_image_display = tk.Label(main_frame, bg="#1e1e1e")
    selected_image_display.pack(pady=(0, 0),padx=(950, 0))  # Add some padding above the label

    # Image selection handler
    def select_image(image_path):
        global true_img
        true_img = image_path
        surveillance_button.config(state=tk.NORMAL)

        # Update the label with the selected image name (without extension)
        name_without_extension = os.path.splitext(os.path.basename(image_path))[0]
        selected_image_label.config(text=f"➜ {name_without_extension}")  # Update the label text
        print(f"Selected image: {true_img}")

        # Update the selected image display
        try:
            img = Image.open(image_path)
            img = img.resize((400, 400), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            image_refs.append(img_tk)  # Store reference to avoid garbage collection
            selected_image_display.config(image=img_tk)
            selected_image_display.image = img_tk  # Keep a reference to avoid garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image for display: {e}")

    # Display images as selectable buttons in a grid
    for index, file in enumerate(image_files):
        img_path = os.path.join(persons_folder, file)
        print(f"Loading image: {img_path}")

        try:
            # Open and resize the image
            img = Image.open(img_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)

            # Store the reference to avoid garbage collection
            img_tk = ImageTk.PhotoImage(img)
            image_refs.append(img_tk)

            # Create a button for each image
            img_button = tk.Button(
                scrollable_frame, image=img_tk,
                command=lambda path=img_path: select_image(path),
                relief="raised", bd=2
            )

            # Place the button in the grid
            img_button.grid(row=(index // 4) + 1, column=index % 4, padx=10, pady=10)  # 4 columns

            # Remove the extension from the file name
            name_without_extension = os.path.splitext(file)[0]

            # Display the name of the image below the button
            name_label = tk.Label(scrollable_frame, text=name_without_extension, bg="#1e1e1e", fg="white", font=(15))
            name_label.grid(row=(index // 4) + 1, column=index % 4, padx=15, pady=(0, 10), sticky='n')

        except Exception as e:
            messagebox.showerror("Error", f"Error loading image {file}: {e}")

    # Surveillance button (initially disabled)
    surveillance_button = tk.Button(
        main_frame, text="Surveillance", bg="#D46083", fg="white", state=tk.DISABLED,
        font=("Arial", 20), width=35, height=2, relief="raised", bd=3
    )
    
    # Center the surveillance button
    surveillance_button.place(relx=.75, rely=0.75, anchor='center')
   
   
    def open_surveillance_canvas():
        
             # Ensure this variable is correctly assigned
            print(f"Finding: {true_img}")
            image_path = true_img
            print(f"Finding ---------: {image_path}")
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            print(f"Finding ---------: {image_name}")
            recipient_email = user_id
            print(os.path.exists(true_img))
            destination = "true_img.png"  # Target file in the root directory
    
            # Copy or rename the input file to "true_img.png"
            if os.path.exists(true_img):
                shutil.copy(true_img, destination)  # Copy the file to true_img.png
                print(f"File {true_img} copied as {destination}.")
            else:
                print(f"Error: {true_img} not found!")
                return
        
            subprocess.Popen(['python', 'recogggg1.py', true_img, recipient_email, image_name])

    surveillance_button.config(command=open_surveillance_canvas)
#----------------------------------------------------------------------------------------------------------------------------TRAINING-----------------------------------




#---------------------------------------------------------------------------------------------------------------------------HOME SCREEN-------------------------------------
def back_to_home(*caps):
    """Releases video captures and reloads the home screen."""
    global bg_label, bg_image

    # Release all video captures
    for cap in caps:
        cap.release()
    
    # Clear all widgets in the home screen
    for widget in home_screen.winfo_children():
        widget.destroy()

    # Reapply the background image
    bg_label = tk.Label(home_screen, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    screen_width = home_screen.winfo_screenwidth()
    screen_height = home_screen.winfo_screenheight()
    load_home_content(screen_width, screen_height)

import siamese




import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

def show_home_screen():
    global home_screen, bg_image, sidebar_window

    home_screen = tk.Tk()
    home_screen.title("Trinetra - 'More than Meets the Eye'")

    screen_width = home_screen.winfo_screenwidth()
    screen_height = home_screen.winfo_screenheight()
    home_screen.geometry(f"{screen_width}x{screen_height}")

    try:
        bg_image = Image.open("./assets/eye.jpg")
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(home_screen, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading background image: {e}")

    load_home_content(screen_width, screen_height)

    home_screen.mainloop()


def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def on_hover(event, canvas, button, original_color):
    canvas.itemconfig(button, fill="black")


def off_hover(event, canvas, button, original_color):
    canvas.itemconfig(button, fill=original_color)


def load_home_content(screen_width, screen_height):
    global sidebar_window

    canvas = tk.Canvas(home_screen, width=screen_width, height=screen_height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(screen_width // 2, screen_height // 2, image=bg_image, anchor="center")

    canvas.create_text(screen_width // 2, screen_height // 4, text="Welcome to TRINETRA", font=("Courier New", 50, "bold"), fill="white", anchor="center")
    canvas.create_text(screen_width // 2, screen_height // 3, text="Eyes of Justice", font=("Georgia", 24), fill="white", anchor="center")

    custom_font = font.Font(family="Courier New", size=20, weight="bold")

    button_width = 340
    button_height = 95
    button_y = screen_height // 1.5

    button_bg = "#6A00FF"
    button_fg = "white"

    container_width = button_width * 3 + 80
    container_height = button_height + 40

    container_x = screen_width // 2 - container_width // 2
    container_y = button_y - container_height // 2

    button_container = canvas.create_rectangle(container_x, container_y,
                                               container_x + container_width, container_y + container_height,
                                               outline="#FF00FF", width=3, fill="black")

    button_spacing = (container_width - button_width * 3) // 4

    button2_x = container_x + button_spacing
    button3_x = button2_x + button_width + button_spacing
    button4_x = button3_x + button_width + button_spacing

    button2_rect = canvas.create_rectangle(button2_x, button_y - button_height // 2,
                                           button2_x + button_width, button_y + button_height // 2,
                                           fill=button_bg, outline="#FF00FF", width=3)
    button3_rect = canvas.create_rectangle(button3_x, button_y - button_height // 2,
                                           button3_x + button_width, button_y + button_height // 2,
                                           fill=button_bg, outline="#FF00FF", width=3)
    button4_rect = canvas.create_rectangle(button4_x, button_y - button_height // 2,
                                           button4_x + button_width, button_y + button_height // 2,
                                           fill=button_bg, outline="#FF00FF", width=3)

    button2_text = canvas.create_text(button2_x + button_width // 2, button_y, text="GENERATE DATASET", font=custom_font, fill=button_fg)
    button3_text = canvas.create_text(button3_x + button_width // 2, button_y, text="TRAIN", font=custom_font, fill=button_fg)
    button4_text = canvas.create_text(button4_x + button_width // 2, button_y, text="SURVEILLANCE", font=custom_font, fill=button_fg)

    canvas.tag_bind(button2_rect, "<Button-1>", lambda event: show_generate_dataset_screen())
    canvas.tag_bind(button3_rect, "<Button-1>", lambda event: siamese.train())
    canvas.tag_bind(button4_rect, "<Button-1>", lambda event: image_surveillance())

    canvas.tag_bind(button2_text, "<Button-1>", lambda event: show_generate_dataset_screen())
    canvas.tag_bind(button3_text, "<Button-1>", lambda event: siamese.train())
    canvas.tag_bind(button4_text, "<Button-1>", lambda event: image_surveillance())

    canvas.tag_bind(button2_rect, "<Enter>", lambda event: on_hover(event, canvas, button2_rect, button_bg))
    canvas.tag_bind(button3_rect, "<Enter>", lambda event: on_hover(event, canvas, button3_rect, button_bg))
    canvas.tag_bind(button4_rect, "<Enter>", lambda event: on_hover(event, canvas, button4_rect, button_bg))

    canvas.tag_bind(button2_rect, "<Leave>", lambda event: off_hover(event, canvas, button2_rect, button_bg))
    canvas.tag_bind(button3_rect, "<Leave>", lambda event: off_hover(event, canvas, button3_rect, button_bg))
    canvas.tag_bind(button4_rect, "<Leave>", lambda event: off_hover(event, canvas, button4_rect, button_bg))

    sidebar_button = tk.Button(home_screen, text="☰", font=("Arial", 20), bg="#ff0099", fg="white",
                               activebackground="#00CCFF", activeforeground="black", command=toggle_sidebar)
    sidebar_button.place(relx=0.98, rely=0.5, anchor="center")

    sidebar_window = tk.Toplevel(home_screen)
    sidebar_window.geometry("800x0")
    sidebar_window.withdraw()
    sidebar_window.configure(bg="#2b2b2b")
    sidebar_window.overrideredirect(True)

    sidebar_x = (screen_width // 2) - 400
    sidebar_y = (screen_height // 2) - 350
    sidebar_window.geometry(f"800x0+{sidebar_x}+{sidebar_y}")

    sidebar_border = tk.Frame(sidebar_window, bg="black", bd=8, relief="solid", padx=10, pady=10)
    sidebar_border.pack(fill="both", expand=True, padx=15, pady=15)

    sidebar_title = tk.Label(sidebar_border, text="TRINETRA MENU", font=("Courier New", 18, "bold"), fg="white", bg="#2b2b2b")
    sidebar_title.pack(pady=15)

    desc_frame = tk.Frame(sidebar_border, bg="#1e1e1e", padx=15, pady=15, bd=3, relief="ridge")
    desc_frame.pack(fill="both", expand=True, padx=10, pady=10)

    desc_text = """1. Generate Dataset – This feature creates a comprehensive dataset of images based on the provided input image. It captures various facial angles, expressions, and lighting conditions to build a diverse and well-rounded collection. 

2. Train – The training module uses the generated dataset to train an advanced facial recognition model. By learning from multiple images, the model becomes capable of identifying unique facial features, distinguishing individuals with high precision, and improving its recognition capabilities over time.

3. Surveillance – This feature enables real-time monitoring using connected camera systems. It tracks individuals in live video feeds and triggers instant alerts if suspicious activity or matches with a target face are detected. This makes it ideal for security, surveillance, and monitoring applications.
"""
    desc_label = tk.Label(desc_frame, text=desc_text, wraplength=650, justify="left", font=("Courier New", 15, "bold"), fg="white", bg="#1e1e1e")
    desc_label.pack(expand=True)

def toggle_sidebar():
    global sidebar_window
    if sidebar_window.winfo_ismapped():
        for i in range(700, 0, -20):
            sidebar_window.geometry(f"800x{i}")
            sidebar_window.update()
        if sidebar_window and sidebar_window.winfo_exists():
             sidebar_window.withdraw()

    else:
        sidebar_window.deiconify()
        for i in range(0, 700, 20):
            sidebar_window.geometry(f"800x{i}")
            sidebar_window.update()



#----------------------------------------------------------------------------------------------------------------------------LOGIN SCREEN -------------------------------------------

def validate_login(login_screen, user_entry, password_entry):
    """Validates login credentials and proceeds to home screen if correct."""
    global user_id
    user_id = user_entry.get()
    password = password_entry.get()
    
    if  password == "1234":
        login_screen.destroy()  # Close login screen
        show_home_screen()  # Open home screen
    else:
        messagebox.showerror("Login Failed", "Invalid User ID or Password")

def on_close():
    """Handles login screen close event."""
    global login_screen
    if login_screen is not None:
        login_screen.destroy()
        login_screen = None

def show_login_screen():
    """Displays the login screen."""
    global login_screen
    if login_screen is not None and login_screen.winfo_exists():
        return

    login_screen = tk.Tk()
    login_screen.title("Login - Trinetra")

    # Center window
    screen_width = login_screen.winfo_screenwidth()
    screen_height = login_screen.winfo_screenheight()
    window_width, window_height = 1400, 800
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    login_screen.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    login_screen.configure(bg="#1e1e1e")

    # Load background image
    bg_image = Image.open("./assets/eye2.jpg").resize((1400, 800), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Canvas setup
    canvas = tk.Canvas(login_screen, width=1400, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(700, 400, image=bg_photo, anchor="center")

    offset_x = 325

    def create_rounded_rect(canvas, x1, y1, x2, y2, radius, color, outline_color=""):
        """Creates a rounded rectangle with arcs and rectangles."""
        if outline_color:
            for dx, dy, start in [(x1-4, y1-4, 90), (x2-2*radius-4, y1-4, 0), 
                                  (x2-2*radius-4, y2-2*radius-4, 270), (x1-4, y2-2*radius-4, 180)]:
                canvas.create_arc(dx, dy, dx+2*radius+8, dy+2*radius+8, start=start, extent=90, fill=outline_color, outline=outline_color)
            canvas.create_rectangle(x1+radius, y1-4, x2-radius, y2+4, fill=outline_color, outline=outline_color)
            canvas.create_rectangle(x1-4, y1+radius, x2+4, y2-radius, fill=outline_color, outline=outline_color)

        for dx, dy, start in [(x1, y1, 90), (x2-2*radius, y1, 0), 
                              (x2-2*radius, y2-2*radius, 270), (x1, y2-2*radius, 180)]:
            canvas.create_arc(dx, dy, dx+2*radius, dy+2*radius, start=start, extent=90, fill=color, outline=color)
        canvas.create_rectangle(x1+radius, y1, x2-radius, y2, fill=color, outline=color)
        canvas.create_rectangle(x1, y1+radius, x2, y2-radius, fill=color, outline=color)

    create_rounded_rect(canvas, 400 + offset_x, 200, 1000 + offset_x, 600, 50, "#1e1e1e")

    # Placeholder functions
    def on_entry_click(event, entry, default_text, hide=False):
        """Clears entry text when clicked if it's the placeholder."""
        if entry.get() == default_text:
            entry.delete(0, tk.END)
            entry.config(fg="black", show="•" if hide else "")

    def on_focus_out(event, entry, default_text):
        """Restores placeholder text if the entry is empty."""
        if not entry.get():
            entry.insert(0, default_text)
            entry.config(fg="grey", show="" if default_text == "Password" else "")

    create_rounded_rect(canvas, 450 + offset_x, 380, 950 + offset_x, 430, 25, "white", outline_color="#0066cc")
 # Adjust position as needed
      
    # User ID Entry
    user_entry = tk.Entry(login_screen, font=("Courier New", 14), bg="white", fg="grey", relief="flat", borderwidth=0, width=28)
    user_entry.insert(0, "User ID")
    user_entry.bind("<FocusIn>", lambda event: on_entry_click(event, user_entry, "User ID"))
    user_entry.bind("<FocusOut>", lambda event: on_focus_out(event, user_entry, "User ID"))
    user_entry.place(x=465 + offset_x, y=310, height=30)

    create_rounded_rect(canvas, 450 + offset_x, 300, 950 + offset_x, 350, 25, "white", outline_color="#0066cc")

    # Password Entry
    password_entry = tk.Entry(login_screen, font=("Courier New", 14), bg="white", fg="grey", relief="flat", borderwidth=0, width=24)
    password_entry.insert(0, "Password")
    password_entry.bind("<FocusIn>", lambda event: on_entry_click(event, password_entry, "Password", hide=True))
    password_entry.bind("<FocusOut>", lambda event: on_focus_out(event, password_entry, "Password"))
    password_entry.place(x=465 + offset_x, y=390, height=30)
    
    

    # Toggle password visibility
    def toggle_password():
        if password_entry["show"] == "":
            password_entry.config(show="•")
            eye_button.config(text="👁")
        else:
            password_entry.config(show="")
            eye_button.config(text="👁‍🗨")

    # Eye Button for Password
    eye_button = tk.Button(login_screen, text="👁", font=("Arial", 12), bg="white", borderwidth=0, command=toggle_password, relief="flat")
    eye_button.place(x=915 + offset_x, y=390, height=30, width=30)

    # Titles
    canvas.create_text(300, 325, text="TRINETRA", font=("Arial Black", 48, "bold"), fill="white", anchor="center")
    canvas.create_text(300, 400, text="Eyes of Justice", font=("Georgia", 24), fill="white", anchor="center")

    # Create login button function
    def create_rounded_button(canvas, x1, y1, x2, y2, radius, text, command):
        create_rounded_rect(canvas, x1, y1, x2, y2, radius, "white", outline_color="#0066cc")
        button = tk.Button(login_screen, text=text, font=("Poppins", 14), bg="white", fg="black", relief="flat", borderwidth=0, width=15, command=command)
        button.place(x=x1 + 15, y=y1 + 5, width=(x2 - x1) - 30, height=(y2 - y1) - 10)

    # Login button
    login_button = create_rounded_button(canvas, 550 + offset_x, 470, 850 + offset_x, 520, 20, "Login", lambda: validate_login(login_screen, user_entry, password_entry))

    # Function to validate login on Enter key
    def validate_login_from_entry(event=None):
        validate_login(login_screen, user_entry, password_entry)

    # Bind Enter key to login
    login_screen.bind("<Return>", validate_login_from_entry)

    login_screen.bg_photo = bg_photo
    login_screen.protocol("WM_DELETE_WINDOW", on_close)
    login_screen.mainloop()

 #----------------------------------------------------------------------------------------SCREEN-1--------------------------------------------------
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



def navigate_to_login():
    splash_screen.destroy()  # Close the splash screen
    show_login_screen()  # Open the login screen


# Create and configure the splash screen window
splash_screen = tk.Tk()
splash_screen.title("TRINETRA")  # Title for the splash screen
splash_screen.geometry("700x800")  # Set splash screen dimensions for appearance
splash_screen.overrideredirect(True)  # Remove window decorations (e.g., title bar) for a cleaner look

# Center the splash screen on the user's display
screen_width = splash_screen.winfo_screenwidth()
screen_height = splash_screen.winfo_screenheight()
x = (screen_width // 2) - (700 // 2)  # Calculate x position to center horizontally
y = (screen_height // 2) - (800 // 2)  # Calculate y position to center vertically
splash_screen.geometry(f"700x800+{x}+{y}")  # Set the geometry of the splash screen with calculated position

# Set background color of the splash screen and load the application logo
splash_screen.configure(bg='#1e1e1e')  # Dark gray background for splash screen
logo_image = tk.PhotoImage(file="./assets/eye.png")  # Load the logo image
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
splash_screen.after(3500, navigate_to_login)  # Navigate to home after 3.5 seconds

# Display the splash screen and begin the application's main event loop
splash_screen.mainloop()    

#------------------------------------------------------------------------------------------------------------------------------------------------------


    








