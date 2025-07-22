import tkinter as tk
import time
import pygame
import threading
from datetime import datetime
from PIL import Image, ImageTk
import tkinter.font as tkFont
import keyboard  


class erpApp(tk.Tk):
    def __init__(self):
        super().__init__()

        window_width = 350
        window_height = 140
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = screen_width - window_width
        y = 0
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.configure(bg="#000033")
        self.resizable(False, False)
        self.wm_attributes("-topmost", 1)
        self.overrideredirect(True)

        self.elapsed_start_time = time.time()
        self.is_colon_visible = True
        self.welcome_screen()

        self.balance_file = "balance.txt"
        self.balance = self.load_balance()

        self.digital_font = tkFont.Font(family="Courier", size=14, weight="bold")

        self.is_parking_active = False
        self.parking_start_time = None
        self.parking_fee = 0.00

        pygame.mixer.init()

        threading.Thread(target=self.register_global_hotkey, daemon=True).start()

    def register_global_hotkey(self):
        def on_hotkey():
            print("[DEBUG] Ctrl+8 pressed, toggling parking mode")
            self.after(0, self.toggle_parking_mode)
        keyboard.add_hotkey('ctrl+8', on_hotkey)
        keyboard.wait()

    def welcome_screen(self):
        self.clear_screen()
        self.geometry("350x140")
        image_path = r"C:\_projects\taxi_meter_interface\asserts\welcome_screen.png"
        image = Image.open(image_path).resize((350, 140))
        self.tk_image = ImageTk.PhotoImage(image)
        label = tk.Label(self, image=self.tk_image, borderwidth=0)
        label.pack()
        self.after(700, self.show_main_menu)

    def show_main_menu(self):
        self.clear_screen()

        self.top_bar_frame = tk.Frame(self, bg="#000033")
        self.top_bar_frame.pack(fill="x")

        self.top_left_frame = tk.Frame(self.top_bar_frame, bg="#000033")
        self.top_left_frame.pack(side="left", padx=10, anchor="n")

        logo_path = r"C:\_projects\taxi_meter_interface\asserts\cepas_logo.png"
        logo_img = Image.open(logo_path).resize((30, 30))
        self.logo_photo = ImageTk.PhotoImage(logo_img)

        self.logo_label = tk.Label(self.top_left_frame, image=self.logo_photo, bg="#000033")
        self.logo_label.pack(side="left")

        balance_amount = f"${self.balance:.2f}"
        self.balance_label = tk.Label(self.top_left_frame, text=balance_amount, fg="white", bg="#000033", font=("Helvetica", 10))
        self.balance_label.pack(side="left", padx=5)

        self.top_right_frame = tk.Frame(self.top_bar_frame, bg="#000033")
        self.top_right_frame.pack(side="right", padx=0, anchor="n")

        menu_logo_path = r"C:\_projects\taxi_meter_interface\asserts\hamburger_main_menu_logo.png"
        menu_img = Image.open(menu_logo_path).resize((30, 30))
        self.menu_photo = ImageTk.PhotoImage(menu_img)

        self.menu_label = tk.Label(self.top_right_frame, image=self.menu_photo, bg="#000033", cursor="hand2")
        self.menu_label.pack()

        # Disable menu during parking
        if not self.is_parking_active:
            self.menu_label.bind("<Button-1>", lambda e: self.show_settings_menu())
        else:
            self.menu_label.bind("<Button-1>", lambda e: print("Parking in progress – Menu disabled"))

        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%a, %d/%m/%Y")

        self.info_frame = tk.Frame(self, bg="#000033")
        self.info_frame.pack(expand=True, fill='both')

        self.time_label = tk.Label(self.info_frame, text=f"{time_str}", fg="white", bg="#000033", font=("Helvetica", 40))
        self.time_label.pack(pady=(0, 0))

        self.date_label = tk.Label(self.info_frame, text=f"{date_str}", fg="white", bg="#000033", font=("Helvetica", 10))
        self.date_label.pack()

        # Add parking status label if active
        if self.is_parking_active:
            parking_status = tk.Label(self.info_frame, text="PARKING MODE ACTIVE", fg="red", bg="#000033", font=("Helvetica", 10, "bold"))
            parking_status.pack(pady=(5, 0))

        self.update_time()
        self.update_balance_label()

    def toggle_parking_mode(self):
        print(f"[DEBUG] Toggling parking mode. is_parking_active: {self.is_parking_active}")
        if not self.is_parking_active:
            self.start_parking_mode()
        else:
            self.end_parking_mode()

    def show_settings_menu(self):
        self.clear_screen()
        label = tk.Label(self, text="Settings Menu (Placeholder)", bg="#000033", fg="white", font=("Helvetica", 12))
        label.pack(pady=30)
        back_btn = tk.Button(self, text="Back", command=self.show_main_menu)
        back_btn.pack()

    def start_parking_mode(self):
        if self.is_parking_active:
            return
        self.is_parking_active = True
        self.parking_start_time = time.time()
        self.show_parking_start_screen()

    def end_parking_mode(self):
        if not self.is_parking_active:
            return
        self.is_parking_active = False
        parking_duration = time.time() - self.parking_start_time
        minutes = parking_duration / 30  # Use float division to get partial minutes
        self.parking_fee = round(minutes * 0.0214, 2)
        self.show_parking_fee_screen()

    def show_parking_start_screen(self):
        self.play_exit_sound()
        self.clear_screen()
        label1 = tk.Label(self, text="EPS Car Park In Operation", fg="red", bg="#000033", font=self.digital_font)
        label1.pack(pady=(20, 5))
        label2 = tk.Label(self, text="Welcome to UA1 Car Park", fg="red", bg="#000033", font=self.digital_font)
        label2.pack()

        # Go back to main menu after 5 seconds (but still in parking mode)
        self.after(5000, self.show_main_menu)

    def show_parking_fee_screen(self):
        self.clear_screen()
        self.play_exit_sound()
        label1 = tk.Label(self, text=f"Fee: ${self.parking_fee:.2f}", fg="red", bg="#000033", font=self.digital_font)
        label1.pack(pady=(20, 5))
        label2 = tk.Label(self, text="Insert/Tap Card", fg="red", bg="#000033", font=self.digital_font)
        label2.pack()

        if self.parking_fee <= self.balance:
            self.balance -= self.parking_fee
            self.save_balance()
            self.update_balance_label()

        self.after(5000, self.show_main_menu)

    def play_exit_sound(self):
        try:
            pygame.mixer.music.load("C:/Users/Chin Soon/Documents/audio/erp_sound.mp3")
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    def update_balance_label(self):
        if hasattr(self, "balance_label") and self.balance_label.winfo_exists():
            self.balance_label.config(text=f"${self.balance:.2f}")

    def quit_app(self):
        self.clear_screen()
        self.geometry("350x140")
        image_path = r"C:\_projects\taxi_meter_interface\asserts\goodbye.png"
        image = Image.open(image_path).resize((350, 140))
        self.tk_image = ImageTk.PhotoImage(image)
        label = tk.Label(self, image=self.tk_image, borderwidth=0)
        label.pack()
        self.after(700, self.destroy)

    def load_balance(self):
        try:
            with open(self.balance_file, "r") as file:
                return float(file.read())
        except (FileNotFoundError, ValueError):
            return 0.00

    def save_balance(self):
        with open(self.balance_file, "w") as file:
            file.write(str(self.balance))

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
