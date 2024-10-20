import tkinter as tk
from tkinter import ttk
import time

# Function to close the splash screen and open the home screen
def navigate_to_home():
    splash_screen.destroy()  # Close the splash screen
    show_home_screen()  # Open the home screen

# Function to simulate a loader (progress bar)
def run_loader():
    progress['value'] = 0
    max_value = 100
    for i in range(max_value + 1):
        time.sleep(0.015)  # Adjust the speed of the progress bar for 1.5 seconds
        progress['value'] = i  # Update progress bar
        splash_screen.update_idletasks()  # Refresh the splash screen

# Function to create and show the home screen
def show_home_screen():
    home_screen = tk.Tk()
    home_screen.title("Trinetra - 'More than Meets the Eye'")  # Set the title

    # Set home screen to full screen and dark background
    home_screen.geometry(f"{home_screen.winfo_screenwidth()}x{home_screen.winfo_screenheight()}")  # Full screen
    home_screen.configure(bg='#1e1e1e')  # Dark background

    # Load logo image for the home screen
    logo_image = tk.PhotoImage(file="trinetra.png")  # Replace 'trinetra.png' with your logo file
    home_screen.iconphoto(False, logo_image)  # Set the logo as the window icon

    # Create and display the logo at the top of the home screen
    logo_label = tk.Label(home_screen, image=logo_image, bg='#1e1e1e')
    logo_label.pack(pady=(2,2))    
    # Welcome message
    home_label = tk.Label(home_screen, text="Welcome Home User!", font=("Arial", 15), bg='#1e1e1e', fg='white')
    home_label.pack(pady=(1,3))
    description_label = tk.Label(home_screen, text="1. Face Sketch:\nCreates a digital sketch using facial features for identification.\n\n"
                                                   "2. Surveillance:\nUpload a photo, track individuals through surveillance cameras.\n"
                                                   "Alerts authorities with location if detected.",
                                 font=("Arial", 12), bg='lightgrey', fg='black', anchor="w", justify="left")
    description_label.pack(padx=20, pady=20)


    # Create a frame to hold the buttons
    button_frame = tk.Frame(home_screen,bg='#1e1e1e')
    button_frame.pack(pady=30)# Add some vertical padding
    
    # Create two buttons with the warning style and place them horizontally
    button1 = tk.Button(button_frame, text=" FACE SKETCH ",command=lambda:button_action(1), font="Arial 15 bold", padx=10, bg="#f7a014",
         fg="white", pady=5, bd=10, highlightthickness=0, activebackground="#091428",
         activeforeground="#1e1e1e")
    button1.pack(side=tk.LEFT, padx=(20, 38), anchor='w')  # Add horizontal padding between buttons
    button2 = tk.Button(button_frame, text=" SURVILANCE  ",command=lambda:button_action(1), font="Arial 15 bold", padx=20, bg="#f7a014",
         fg="white", pady=5, bd=10, highlightthickness=0, activebackground="#091428",
         activeforeground="#1e1e1e")
    button2.pack(side=tk.LEFT, padx=(38, 20), anchor='e')  # Add horizontal padd
    home_screen.mainloop()
def button_action(button_number):
    print(f"Button {button_number} clicked!")
# Create the splash screen
splash_screen = tk.Tk()
splash_screen.title("Splash Screen")
splash_screen.geometry("800x700")  # Adjust the size to fit content
splash_screen.overrideredirect(True)  # Remove window decorations

# Center the splash screen on the screen
screen_width = splash_screen.winfo_screenwidth()  # Get screen width
screen_height = splash_screen.winfo_screenheight()  # Get screen height
x = (screen_width // 2) - (800 // 2)  # Center x coordinate
y = (screen_height // 2) - (700 // 2)  # Center y coordinate
splash_screen.geometry(f"800x700+{x}+{y}")  # Set the geometry

# Set dark background color for the splash screen
splash_screen.configure(bg='#1e1e1e')  # Dark background (hex color for dark gray)

# Load logo image for the splash screen
logo_image = tk.PhotoImage(file="trinetra.png")  # Replace 'trinetra.png' with your logo file
splash_screen.iconphoto(False, logo_image)  # Set the logo as the window icon

# Create and display the logo, brand name, and slogan
logo_label = tk.Label(splash_screen, image=logo_image, bg='#1e1e1e')
logo_label.pack(pady=10)

brand_name_label = tk.Label(splash_screen, text="TRINETRA", font=("Arial", 20, "bold"), fg="white", bg='#1e1e1e')
brand_name_label.pack()

slogan_label = tk.Label(splash_screen, text="More Than Meets the Eye", font=("Arial", 12, "italic"), fg="white", bg='#1e1e1e')
slogan_label.pack(pady=5)

# Splash screen content - progress bar
progress = ttk.Progressbar(splash_screen, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress.pack(pady=20)

# Start the loader in the splash screen
splash_screen.after(100, run_loader)

# After 1.5 seconds, navigate to the home screen
splash_screen.after(3500, navigate_to_home)

# Show the splash screen
splash_screen.mainloop()
