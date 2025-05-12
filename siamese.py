import tkinter as tk
from tkinter import ttk
import threading
import utils
import numpy as np
from keras.layers import Input, Lambda
from keras.models import Model
from keras.callbacks import Callback
import bim
import os

class TQDMProgressBar(Callback):
    def __init__(self, gui_root, total_epochs):
        super().__init__()
        self.gui_root = gui_root
        self.total_epochs = total_epochs

        # Style configuration
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Cyberpunk.Horizontal.TProgressbar", 
                        troughcolor="#222", background="#0ff", thickness=12)

        # Set window size and center it
        window_width = 500
        window_height = 200
        screen_width = self.gui_root.winfo_screenwidth()
        screen_height = self.gui_root.winfo_screenheight()
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        self.gui_root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Frame to center elements
        self.frame = tk.Frame(self.gui_root, bg="#120e26")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Label for loading and training phases
        self.label = tk.Label(self.frame, text="Loading Data...", fg="white", bg="#120e26", font=("Courier New", 12))
        self.label.pack(pady=10)

        # Loading Bar (Indeterminate Mode)
        self.loading_bar = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="indeterminate",
                                           style="Cyberpunk.Horizontal.TProgressbar")
        self.loading_bar.pack(pady=10)
        self.loading_bar.start(10)  

        # Training Progress Bar (Determinate Mode)
        self.progressbar = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate",
                                           style="Cyberpunk.Horizontal.TProgressbar")
        self.progressbar["maximum"] = total_epochs
        self.progressbar.pack_forget()

    def switch_to_training_mode(self):
        """Switch from loading bar to training progress bar."""
        self.label.config(text="Training Progress", font=("Courier New", 12))
        self.loading_bar.stop()  
        self.loading_bar.pack_forget()  
        self.progressbar.pack(pady=10)  

    def on_epoch_end(self, epoch, logs=None):
        """Update progress at the end of each epoch."""
        self.progressbar["value"] = epoch + 1
        self.gui_root.update_idletasks()

def train():
    root = tk.Tk()
    root.title("Training Progress")
    root.configure(bg='#120e26')

    total_epochs = 10
    progress_callback = TQDMProgressBar(root, total_epochs)

    def train_model():
        """Phase 1: Loading Data While bim.main() Executes"""

        """Phase 2: Training"""
        faces_dir = 'dataset/'

        try:
            (X_train, Y_train), (X_test, Y_test) = utils.get_data(faces_dir)
        except Exception as e:
            print(f"Error loading dataset: {e}")
            root.after(100, root.destroy)  # Ensure window closes even if error occurs
            return

        num_classes = len(np.unique(Y_train))
        input_shape = X_train.shape[1:]
        shared_network = utils.create_shared_network(input_shape)

        input_top = Input(shape=input_shape)
        input_bottom = Input(shape=input_shape)
        output_top = shared_network(input_top)
        output_bottom = shared_network(input_bottom)
        distance = Lambda(utils.euclidean_distance, output_shape=(1,))([output_top, output_bottom])
        model = Model(inputs=[input_top, input_bottom], outputs=distance)

        training_pairs, training_labels = utils.create_pairs(X_train, Y_train, num_classes=num_classes)
        model.compile(loss=utils.contrastive_loss, optimizer='adam', metrics=[utils.accuracy])

        model.fit([training_pairs[:, 0], training_pairs[:, 1]], training_labels,
                  batch_size=128,
                  epochs=total_epochs,
                  callbacks=[progress_callback])

        model.save('siamese_nn.h5')
        print("✅ Model training complete and saved to 'siamese_nn.h5'")

        root.after(100, root.destroy)  # ✅ Properly close the window after training completes

    # Run the training in a separate thread so UI doesn't freeze
    training_thread = threading.Thread(target=train_model)
    training_thread.start()

    root.mainloop()  # Keep UI responsive

if __name__ == '__main__':
    train()
