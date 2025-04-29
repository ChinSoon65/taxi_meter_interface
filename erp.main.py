import tkinter as tk
import random
import time
import pygame
import threading
import winsound
from datetime import datetime


class erpApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ERP")
        self.geometry("480x320")
        self.configure(bg="#ADD8E6")  # Dark mode background
        self.resizable(True, True)
        self.wm_attributes("-topmost", 1)  # Keep the window always on top

        self.elapsed_start_time = time.time()
        self.is_colon_visible = True  # Track whether the colon is visible

        self.welcome_screen()

    def welcome_screen(self):
        self.clear_screen()

        label = tk.Label(self, text="WELCOME", font=("Ubuntu Light", 24, "bold"), bg="#00008B", fg="white")
        label.pack(expand=True)

        self.after(2500, self.show_main_menu)

    def show_main_menu(self):

        self.clear_screen()

        # Display Top Info (Date, Region, Earnings)
        now = datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        self.info_frame = tk.Frame(self, bg="#00008B")
        self.info_frame.pack(pady=10)

        self.date_label = tk.Label(self.info_frame, text=f"Date: {date_str}", fg="white", bg="#00008B", font=("Helvetica", 10))
        self.date_label.grid(row=0, column=0, padx=5)

        # Set time
        current_time = time.strftime("%H:%M:%S")

        self.time_label = tk.Label(self.info_frame, text=f"Time: {current_time}", fg="white", bg="#00008B", font=("Helvetica", 10))
        self.time_label.grid(row=1, column=0, padx=5)


        self.update_time()


    def update_time(self):

        if hasattr(self, "time_label") and self.time_label.winfo_exists():
            current_time = time.strftime("%H:%M:%S")
            self.time_label.config(text=f"Time: {current_time}")
            self.after(1000, self.update_time)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = erpApp()
    app.mainloop()



