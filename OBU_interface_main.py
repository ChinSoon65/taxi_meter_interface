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

        # Set window size
        window_width = 350
        window_height = 140

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set position to top-right
        x = screen_width - window_width
        y = 0
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.configure(bg="#000033")  # Dark mode background
        self.resizable(True, True)
        self.wm_attributes("-topmost", 1)  # Keep the window always on top

        self.overrideredirect(True)

        self.elapsed_start_time = time.time()
        self.is_colon_visible = True  # Track whether the colon is visible
        
        self.welcome_screen() # starting interface
        
        self.is_card_on = True # Sets card to be ON by default for switch_card_payment_image function

        # OBU Balance amount text file
        self.balance_file = "balance.txt"
        self.balance = self.load_balance() 



    def welcome_screen(self):  # starting interface
        self.clear_screen()
        self.geometry("350x140")  # Fixed window size

        # Load and display image
        image_path = r"C:\_projects\taxi_meter_interface\asserts\welcome_screen.png"
        image = Image.open(image_path)
        image = image.resize((350, 140))  # Optional: force-fit to window

        self.tk_image = ImageTk.PhotoImage(image)  # Keep a reference on self
        label = tk.Label(self, image=self.tk_image, borderwidth=0)
        label.pack()

        self.after(700, self.show_main_menu)  

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
        balance_amount = f"${self.balance:.2f}"
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
        balance_amount = f"${self.balance:.2f}"
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
        icon_label_frame.pack(side="left", padx=40)

        logo_path3 = r"C:\_projects\taxi_meter_interface\asserts\setting_gear.png"
        logo_img3 = Image.open(logo_path3).resize((60, 60))

        self.logo_photo3 = ImageTk.PhotoImage(logo_img3)

        # button for the Setting icon (Gear icon) Nd to change from main menu to have a custom menu
        icon_button = tk.Button(icon_label_frame, image=self.logo_photo3, command=self.settings_options,
                        bg="#000033", fg="white", relief="flat", font=("Helvetica", 10))
        icon_button.pack(side="top")  # Stacks on top

        # Text Label
        settings_label = tk.Label(icon_label_frame, text="Settings", bg="#000033", fg="white", font=("Helvetica", 9))
        settings_label.pack(side="top")  # Stacks below

        # New frame for the button, placed to the right of the icon_label_frame
        next_button_frame = tk.Frame(self.middle_bar_frame, bg="#000033")
        next_button_frame.pack(side="left", padx=0)

        logo_quit = r"C:\_projects\taxi_meter_interface\asserts\exit.png"
        logo_quit_img = Image.open(logo_quit).resize((60, 60))

        self.logo_quit = ImageTk.PhotoImage(logo_quit_img)

        next_button = tk.Button(next_button_frame, image=self.logo_quit, command=self.quit_app,
                                bg="#000033", fg="white", relief="flat", font=("Helvetica", 10))
        next_button.pack(side="top")

        quit_text_label = tk.Label(next_button_frame, text="Quit", bg="#000033", fg="white", font=("Helvetica", 9))
        quit_text_label.pack(side="top")

        # Card Payment "ON" button

        # Label for Card Payment icon "ON"
        card_payment_button_label = tk.Frame(self.middle_bar_frame, bg="#000033")
        card_payment_button_label.pack(side="left", padx=20)

        # Load Card Payment icon "ON"
        logo_card_payment_on = r"C:\_projects\taxi_meter_interface\asserts\card_payment_on.png"
        logo_card_payment_on_img = Image.open(logo_card_payment_on).resize((80, 80))
        self.logo_card_payment_on = ImageTk.PhotoImage(logo_card_payment_on_img)

        # Load Card Payment icon "OFF" (preload for switch)
        logo_card_payment_off = r"C:\_projects\taxi_meter_interface\asserts\card_payment_off.png"
        logo_card_payment_off_img = Image.open(logo_card_payment_off).resize((80, 80))
        self.logo_card_payment_off = ImageTk.PhotoImage(logo_card_payment_off_img)

        self.current_logo = self.logo_card_payment_on if self.is_card_on else self.logo_card_payment_off

        self.card_payment_on_button = tk.Button(card_payment_button_label, image=self.current_logo, command=self.switch_card_payment_image,
                                bg="#000033", fg="white", relief="flat", font=("Helvetica", 10))
        self.card_payment_on_button.pack(side="top")

    def switch_card_payment_image(self):
        if self.is_card_on:
            self.card_payment_on_button.config(image=self.logo_card_payment_off)
            self.is_card_on = False
        else:
            self.card_payment_on_button.config(image=self.logo_card_payment_on)
            self.is_card_on = True
            
    # func for Settings (Gear icon png) menu
    def settings_options(self):

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
        balance_amount = f"${self.balance:.2f}"
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






    def quit_app(self):
        self.clear_screen()
        self.geometry("350x140")  # Fixed window size

        # Load and display image
        image_path = r"C:\_projects\taxi_meter_interface\asserts\goodbye.png"
        image = Image.open(image_path)
        image = image.resize((350, 140))  # Optional: force-fit to window

        self.tk_image = ImageTk.PhotoImage(image)  # Keep a reference on self
        label = tk.Label(self, image=self.tk_image, borderwidth=0)
        label.pack()

        self.after(700, self.destroy)  
        
    # load balancing function
    def load_balance(self):
        try:
            with open(self.balance_file, "r") as file:
                return float(file.read())
        except(FileNotFoundError,ValueError):
            return 0.00 # default starting balance
        
    # saving the balance 
    def save_balance(self):
        with open(self.balance_file,"w") as file:
            file.write(str(self.balance))
    



    def update_time(self):
        if hasattr(self, "time_label") and self.time_label.winfo_exists():
            current_time = time.strftime("%I:%M %p")
            self.time_label.config(text=f"{current_time}")
            self.after(100, self.update_time)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = erpApp()
    app.mainloop()



