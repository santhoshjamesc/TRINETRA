from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import random
import os
import threading

# Function to open a file dialog for uploading an image
def upload_image():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:  # Check if a file was selected
        messagebox.showinfo("Selected File", f"You selected: {file_path}")
        show_selected_image(file_path)  # Show the selected image
        # Start the generation of variations in a separate thread
        threading.Thread(target=generate_variations, args=(file_path,), daemon=True).start()
    else:
        messagebox.showwarning("No Selection", "No file was selected.")

# Function to show the selected image in the menu frame
def show_selected_image(file_path):
    # Clear previous image if any
    for widget in menu_frame.winfo_children():
        if isinstance(widget, Label) and widget != upload_button:  # Only clear the image label
            widget.destroy()

    img = Image.open(file_path)
    img.thumbnail((200, 200))  # Resize for display
    img_tk = ImageTk.PhotoImage(img)

    img_label = Label(menu_frame, image=img_tk, bg='#544ecc')  # Set the background color
    img_label.image = img_tk  # Keep a reference to avoid garbage collection
    img_label.pack(pady=8)  # Pack the image label below the upload button

# Function to generate 50 variations of the uploaded image
def generate_variations(file_path):
    # Clear previous variations if any
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Create a directory to save variations
    variations_dir = "image_variations"
    os.makedirs(variations_dir, exist_ok=True)

    # Create a canvas with a scrollbar
    canvas = Canvas(content_frame)
    scrollbar = Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)
    scrollable_frame.configure(bg='#1e1e1e')

    # Configure the scrollable frame
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the canvas and scrollbar
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Generate 50 variations
    for i in range(50):
        img = Image.open(file_path)

        # Create a random variation
        variation_type = random.choice(["rotate", "gray", "flip", "invert"])
        if variation_type == "rotate":
            img = img.rotate(random.randint(0, 360))  # Random rotation
        elif variation_type == "gray":
            img = img.convert("L")  # Convert to grayscale
        elif variation_type == "flip":
            img = ImageOps.mirror(img)  # Flip the image horizontally
        elif variation_type == "invert":
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img = ImageOps.invert(img)  # Invert the colors of the image

        # Save the variation
        variation_file_path = os.path.join(variations_dir, f"variation_{i + 1}.png")
        img.save(variation_file_path)

        # Resize to fit display area
        img.thumbnail((400, 400))  # Display size
        img_tk = ImageTk.PhotoImage(img)

        img_label = Label(scrollable_frame, image=img_tk, bg='#1e1e1e', width=400, height=400)
        img_label.image = img_tk  # Keep a reference to avoid garbage collection
        img_label.grid(row=i // 3, column=i % 3, padx=3, pady=3)  # Arrange in columns

# Create the main window
ws = Tk()
ws.geometry(f"{ws.winfo_screenwidth()}x{ws.winfo_screenheight()}")
ws.title('DATASET MAKER')
ws.configure(bg='#1e1e1e')

# Create a frame for the content
content_frame = Frame(ws, bg='#1e1e1e')
content_frame.pack(side=RIGHT, fill=BOTH, expand=True)

# Create a label for the second page
Label(
    content_frame,
    text="Upload an image to generate image variations",
    padx=20,
    pady=20,
    bg='#1e1e1e',
    fg='white',
    font=("Times bold", 14)
).pack(expand=True, fill=BOTH)

# Create a frame for the menu
menu_frame = Frame(ws, bg='#091428', width=300, height=600)  # Set desired width and height
menu_frame.pack(side=LEFT)  # Fill vertically
menu_frame.pack_propagate(False)

# Create an upload button in the menu and center it
upload_button = Button(menu_frame, text="Upload Image", command=upload_image, bg='#1e1e1e', fg='white', font=("Arial", 12), padx=10, pady=15)
upload_button.pack(expand=True)  # Center the button in the menu frame

# Start the Tkinter event loop
ws.mainloop()
