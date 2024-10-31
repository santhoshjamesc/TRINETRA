import tkinter as tk
from tkinter import ttk, messagebox
import time

# Global variable to hold pages
pages = []

# Function to close the splash screen and open the login screen
def navigate_to_login():
    splash_screen.destroy()  # Close the splash screen
    show_login_screen()  # Open the login screen

# Function to simulate a loader (progress bar)
def run_loader():
    progress['value'] = 0
    max_value = 100
    for i in range(max_value + 1):
        time.sleep(0.015)  # Adjust the speed of the progress bar for 1.5 seconds
        progress['value'] = i  # Update progress bar
        splash_screen.update_idletasks()  # Refresh the splash screen

# Function to create and show the login screen
def show_login_screen():
    login_screen = tk.Tk()
    login_screen.title("Login - Trinetra")
    login_screen.geometry("400x300")  # Set the login screen size

    # Set background color and center the login screen on the screen
    login_screen.configure(bg='#1e1e1e')
    screen_width = login_screen.winfo_screenwidth()
    screen_height = login_screen.winfo_screenheight()
    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (300 // 2)
    login_screen.geometry(f"400x300+{x}+{y}")

    # Label and Entry for User ID
    user_label = tk.Label(login_screen, text="User ID:", font=("Arial", 12), bg='#1e1e1e', fg='white')
    user_label.pack(pady=(30, 5))
    user_entry = tk.Entry(login_screen, font=("Arial", 12))
    user_entry.pack(pady=5)

    # Label and Entry for Password
    password_label = tk.Label(login_screen, text="Password:", font=("Arial", 12), bg='#1e1e1e', fg='white')
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_screen, show='*', font=("Arial", 12))
    password_entry.pack(pady=5)

    # Login button with action to validate user credentials
    login_button = tk.Button(login_screen, text="Login", font=("Arial", 12), command=lambda: validate_login(login_screen, user_entry, password_entry))
    login_button.pack(pady=20)

    login_screen.mainloop()

# Function to validate login credentials
def validate_login(login_screen, user_entry, password_entry):
    user_id = user_entry.get()
    password = password_entry.get()
    
    # Replace these with actual credentials check
    if user_id.strip() and password.strip():  # Check for non-empty input
        login_screen.destroy()  # Close the login screen
        show_home_screen()  # Open the home screen
    else:
        messagebox.showerror("Login Failed", "Invalid User ID or Password")

# Function to create and show the home screen
def show_home_screen():
    global home_screen
    home_screen = tk.Tk()
    home_screen.title("Trinetra - 'More than Meets the Eye'")
    home_screen.geometry(f"{home_screen.winfo_screenwidth()}x{home_screen.winfo_screenheight()}")
    home_screen.configure(bg='#1e1e1e')

    # Load logo image for the home screen
    logo_image = tk.PhotoImage(file="trinetra.png")  # Replace 'trinetra.png' with your logo file
    home_screen.iconphoto(False, logo_image)

    # Display the logo and welcome message
    logo_label = tk.Label(home_screen, image=logo_image, bg='#1e1e1e')
    logo_label.pack(pady=(2, 2))
    home_label = tk.Label(home_screen, text="Welcome Home User!", font=("Arial", 15), bg='#1e1e1e', fg='white')
    home_label.pack(pady=(1, 3))

    description_label = tk.Label(home_screen, text="1. Face Sketch:\nCreates a digital sketch using facial features for identification.\n\n"
                                                   "2. Surveillance:\nUpload a photo, track individuals through surveillance cameras.\n"
                                                   "Alerts authorities with location if detected.",
                                 font=("Arial", 12), bg='lightgrey', fg='black', anchor="w", justify="left")
    description_label.pack(padx=20, pady=20)

    # Create a frame to hold the buttons
    button_frame = tk.Frame(home_screen, bg='#1e1e1e')
    button_frame.pack(pady=30)
    
    # Create two buttons for functionalities
    button1 = tk.Button(button_frame, text=" FACE SKETCH ", command= show_sketch, font="Arial 15 bold", padx=10, bg="#f7a014",
                        fg="white", pady=5, bd=10, highlightthickness=0, activebackground="#091428",
                        activeforeground="#1e1e1e")
    button1.pack(side=tk.LEFT, padx=(20, 38), anchor='w')
    button3 = tk.Button(button_frame, text=" MAKE DATASET  ", command= mk_dataset, font="Arial 15 bold", padx=20, bg="#f7a014",
                        fg="white", pady=5, bd=10, highlightthickness=0, activebackground="#091428",
                        activeforeground="#1e1e1e")
    button3.pack(side=tk.LEFT, padx=(38, 20), anchor='e')
    button2 = tk.Button(button_frame, text=" SURVEILLANCE  ", command=lambda: show_page(1), font="Arial 15 bold", padx=20, bg="#f7a014",
                        fg="white", pady=5, bd=10, highlightthickness=0, activebackground="#091428",
                        activeforeground="#1e1e1e")
    button2.pack(side=tk.LEFT, padx=(38, 20), anchor='e')

    # Create frames for each page
    

    home_screen.mainloop()
def show_sketch():
    import facesketch
def mk_dataset():
    import datasetmaker
    

# Function to create the Face Sketch page

# Function to show the selected page

# Create the splash screen
splash_screen = tk.Tk()
splash_screen.title("Splash Screen")
splash_screen.geometry("800x700")
splash_screen.overrideredirect(True)

# Center the splash screen on the screen
screen_width = splash_screen.winfo_screenwidth()
screen_height = splash_screen.winfo_screenheight()
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (700 // 2)
splash_screen.geometry(f"800x700+{x}+{y}")
splash_screen.configure(bg='#1e1e1e')

# Load logo image for the splash screen
logo_image = tk.PhotoImage(file="trinetra.png")
splash_screen.iconphoto(False, logo_image)

logo_label = tk.Label(splash_screen, image=logo_image, bg='#1e1e1e')
logo_label.pack(pady=10)

brand_name_label = tk.Label(splash_screen, text="TRINETRA", font=("Arial", 20, "bold"), fg="white", bg='#1e1e1e')
brand_name_label.pack()

slogan_label = tk.Label(splash_screen, text="More Than Meets the Eye", font=("Arial", 12, "italic"), fg="white", bg='#1e1e1e')
slogan_label.pack(pady=5)

# Progress bar
progress = ttk.Progressbar(splash_screen, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress.pack(pady=20)

# Start loader and navigate to login screen
splash_screen.after(100, run_loader)
splash_screen.after(3500, navigate_to_login)

splash_screen.mainloop()
