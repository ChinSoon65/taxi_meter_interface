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

        # === Top Bar Frame (holds both left and right sections) ===
        self.top_bar_frame = tk.Frame(self, bg="#000033")
        self.top_bar_frame.pack(fill="x", pady=0)

        # === Top-Left Frame (Logo + Balance) ===
        self.top_left_frame = tk.Frame(self.top_bar_frame, bg="#000033")
        self.top_left_frame.pack(side="left", padx=10, anchor="n")

        # CEPAS Logo (resized to same size as hamburger)
        logo_path = r"C:\_projects\taxi_meter_interface\asserts\cepas_logo.png" 
        logo_img = Image.open(logo_path).resize((30, 30))  # Ensure exact same size
        self.logo_photo = ImageTk.PhotoImage(logo_img)

        self.logo_label = tk.Label(self.top_left_frame, image=self.logo_photo, bg="#000033")
        self.logo_label.pack(side="left", pady=0)

        # Balance label
        balance_amount = "$0.00"
        self.balance_label = tk.Label(self.top_left_frame, text=balance_amount, fg="white", bg="#000033", font=("Helvetica", 10))
        self.balance_label.pack(side="left", padx=5, pady=0)

        # === Top-Right Frame (Hamburger Menu) ===
        self.top_right_frame = tk.Frame(self.top_bar_frame, bg="#000033")
        self.top_right_frame.pack(side="right", padx=0, anchor="n")

        # Hamburger Menu Icon
        menu_logo_path = r"C:\_projects\taxi_meter_interface\asserts\hamburger_main_menu_logo.png"
        menu_img = Image.open(menu_logo_path).resize((30, 30))  # Same size as above
        self.menu_photo = ImageTk.PhotoImage(menu_img)

        self.menu_label = tk.Label(self.top_right_frame, image=self.menu_photo, bg="#000033", cursor="hand2")
        self.menu_label.pack(anchor="n", pady=0)

        self.menu_label.bind("<Button-1>", lambda e: self.obu_menu_settings())

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

    def obu_menu_settings(self, event = None):

        self.clear_screen()

        # Top bar again for consistency
        self.top_bar_frame = tk.Frame(self, bg="#000033")
        self.top_bar_frame.pack(fill="x", pady=0)

        # === Top-Left Frame (Logo + Balance) ===
        self.top_left_frame = tk.Frame(self.top_bar_frame, bg="#000033")
        self.top_left_frame.pack(side="left", padx=10, anchor="n")

        # CEPAS Logo (resized to same size as hamburger)
        logo_path2 = r"C:\_projects\taxi_meter_interface\asserts\cepas_logo.png" 
        logo_img2 = Image.open(logo_path2).resize((30, 30))  # Ensure exact same size
        self.logo_photo2 = ImageTk.PhotoImage(logo_img2)

        self.logo_label = tk.Label(self.top_left_frame, image=self.logo_photo2, bg="#000033")
        self.logo_label.pack(side="left", pady=0)

        # Balance label
        balance_amount = "$0.00"
        self.balance_label = tk.Label(self.top_left_frame, text=balance_amount, fg="white", bg="#000033", font=("Helvetica", 10))
        self.balance_label.pack(side="left", padx=5, pady=0)

        now = datetime.now()

        time_str = now.strftime("%I:%M %p")  # 06:17 PM format

        self.time_label = tk.Label(self.top_bar_frame, text=f"{time_str}", fg="white", bg="#000033", font=("Helvetica", 13))
        self.time_label.place(relx=0.5, rely=0.5, anchor="center")

        self.update_time()

        # === top_right_frame (Logo + Balance) ===
        self.top_right_frame = tk.Frame(self.top_bar_frame, bg="#000033")
        self.top_right_frame.pack(side="right", padx=0, anchor="n")

        # home Logo 
        logo_path = r"C:\_projects\taxi_meter_interface\asserts\home_menu.png" 
        logo_img = Image.open(logo_path).resize((30, 30))  # Ensure exact same size
        self.logo_photo = ImageTk.PhotoImage(logo_img)

        # Home menu button
        back_button = tk.Button(self.top_right_frame, image=self.logo_photo, command=self.show_main_menu, bg="#000033", fg="white", relief="flat", font=("Helvetica", 10))
        back_button.pack(side="right", padx=0)


        # Middle bar again for consistency
        self.middle_bar_frame = tk.Frame(self, bg="#000033")
        self.middle_bar_frame.pack(side="top", fill="x", pady=0)

        icon_label_frame = tk.Frame(self.middle_bar_frame, bg="#000033")
        icon_label_frame.pack(side="left", padx=80)

        logo_path3 = r"C:\_projects\taxi_meter_interface\asserts\setting_gear.png"
        logo_img3 = Image.open(logo_path3).resize((60, 60))

        self.logo_photo3 = ImageTk.PhotoImage(logo_img3)

        icon_button = tk.Button(icon_label_frame, image=self.logo_photo3, command=self.show_main_menu,
                        bg="#000033", fg="white", relief="flat", font=("Helvetica", 10))
        icon_button.pack(side="top")  # Stacks on top

        # Text Label
        settings_label = tk.Label(icon_label_frame, text="Settings", bg="#000033", fg="white", font=("Helvetica", 9))
        settings_label.pack(side="top")  # Stacks below



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



