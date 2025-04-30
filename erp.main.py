import tkinter as tk
import random
import time
import pygame
import threading
import winsound
from datetime import datetime
from PIL import Image, ImageTk

class erpApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ERP")
        self.geometry("350x140")
        self.configure(bg="#000033")  # Dark mode background
        self.resizable(True, True)
        self.wm_attributes("-topmost", 1)  # Keep the window always on top

        self.elapsed_start_time = time.time()
        self.is_colon_visible = True  # Track whether the colon is visible

        self.welcome_screen()

    def welcome_screen(self):
        self.clear_screen()

        label = tk.Label(self, text="WELCOME", font=("Ubuntu Light", 24, "bold"), bg="#000033", fg="white")
        label.pack(expand=True)

        self.after(500, self.show_main_menu)

    def show_main_menu(self):
        self.clear_screen()

        # Loading of Logo
        logo_path = r"C:\_projects\taxi_meter_interface\asserts\cepas_logo.png" 
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((30,30))
        self.logo_photo = ImageTk.PhotoImage(logo_img)

        # === Create Frame for Top-Left Content ===
        self.top_left_frame = tk.Frame(self, bg="#000033")
        self.top_left_frame.pack(anchor="nw", padx=10, pady=0)  # Top-left corner

        # === Logo Label ===
        self.logo_label = tk.Label(self.top_left_frame, image=self.logo_photo, bg="#000033")
        self.logo_label.pack(side="left")

        # === Balance Label ===
        balance_amount = "$0.00"  # this is going to be replaced
        self.balance_label = tk.Label(self.top_left_frame, text=balance_amount, fg="white", bg="#000033", font=("Helvetica", 10))
        self.balance_label.pack(side="left", padx=5)


        now = datetime.now()

        time_str = now.strftime("%I:%M %p")  # 06:17 PM format
        date_str = now.strftime("%a, %d/%m/%Y")  # Tue, 23/04/2024 format

        self.info_frame = tk.Frame(self, bg="#000033")
        self.info_frame.pack(expand=True, fill='both')

        self.time_label = tk.Label(self.info_frame, text=f"{time_str}", fg="white", bg="#000033", font=("Helvetica", 40))
        self.time_label.pack(pady=(0,0))  # Add spacing above and below

        self.date_label = tk.Label(self.info_frame, text=f"{date_str}", fg="white", bg="#000033", font=("Helvetica", 10))
        self.date_label.pack()

        self.update_time()


    def update_time(self):

        if hasattr(self, "time_label") and self.time_label.winfo_exists():
            current_time = time.strftime("%I:%M %p")
            self.time_label.config(text=f"{current_time}")
            self.after(1000, self.update_time)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = erpApp()
    app.mainloop()



