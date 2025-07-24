import tkinter as tk
import random
import time
import pygame
import threading
import winsound
from datetime import datetime

class TaxiMeterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ComfortDelGro Terminal")
        self.geometry("480x320")
        self.configure(bg="#ADD8E6")  # Dark mode background
        self.resizable(True, True)
        self.wm_attributes("-topmost", 1)  # Keep the window always on top

        # Variables
        self.today_earnings = 0.0
        self.current_job = None
        self.elapsed_start_time = None
        self.is_online = False
        self.region = "South"

        self.elapsed_start_time = time.time()
        self.is_colon_visible = True  # Track whether the colon is visible

        # Screens
        self.welcome_screen()

    def play_notification_sound2(self):
        pygame.mixer.init()
        pygame.mixer.music.load("C:/_Projects/taxi_meter_interface/sfx/CN_welcome.mp3")
        pygame.mixer.music.play()  

        self.is_notification_playing = False

    def play_notification_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("C:/_Projects/taxi_meter_interface/sfx/notification.mp3")
        pygame.mixer.music.play()  



    def stop_notification_sound(self):
        pygame.mixer.music.stop()
        self.is_notification_playing = False

    def welcome_screen(self):
        self.clear_screen()

        label = tk.Label(self, text="WELCOME", font=("Ubuntu Light", 24, "bold"), bg="#00008B", fg="white")
        label.pack(expand=True)

        threading.Thread(target=self.play_notification_sound2, daemon=True).start()

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

        self.region_label = tk.Label(self.info_frame, text=f"Region: {self.region}", fg="white", bg="#00008B", font=("Helvetica", 10))
        self.region_label.grid(row=0, column=1, padx=5)

        self.earnings_label = tk.Label(self.info_frame, text=f"Today's Earnings: ${self.today_earnings:.2f}", fg="white", bg="#00008B", font=("Helvetica", 10))
        self.earnings_label.grid(row=0, column=2, padx=5)

        # Set time
        current_time = time.strftime("%H:%M:%S")

        self.time_label = tk.Label(self.info_frame, text=f"Time: {current_time}", fg="white", bg="#00008B", font=("Helvetica", 10))
        self.time_label.grid(row=1, column=0, padx=5)

        # Main Buttons
        self.main_frame = tk.Frame(self, bg="#00008B")
        self.main_frame.pack(pady=20)

        self.status_label = tk.Label(self.main_frame, text="Status: Offline", fg="white", bg="#00008B", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

        self.go_online_button = tk.Button(self.main_frame, text="Go Online", command=self.toggle_online, width=20)
        self.go_online_button.pack(pady=5)

        self.recent_travels_button = tk.Button(self.main_frame, text="Recent Travels (Coming Soon)", width=20, state="disabled")
        self.recent_travels_button.pack(pady=5)

        self.settings_button = tk.Button(self.main_frame, text="Settings (Coming Soon)", width=20, state="disabled")
        self.settings_button.pack(pady=5)

        self.update_time()

    def update_time(self):
        if hasattr(self, "time_label") and self.time_label.winfo_exists():
            current_time = time.strftime("%H:%M:%S")
            self.time_label.config(text=f"Time: {current_time}")
            self.after(1000, self.update_time)

    def toggle_online(self):
        self.is_online = not self.is_online
        if self.is_online:
            self.status_label.config(text="Status: Online")
            self.go_online_button.config(text="Go Offline")
            self.search_for_job()
        else:
            self.status_label.config(text="Status: Offline")
            self.go_online_button.config(text="Go Online")

    def search_for_job(self):
        if not self.is_online:
            return
        # Searching...
        self.status_label.config(text="Status: Searching for Job...")
        delay = random.randint(3000, 4000)  # Random delay between 3-7 seconds
        self.after(delay, self.generate_job_offer)

    def generate_job_offer(self):
        if not self.is_online:
            return

        threading.Thread(target=self.play_notification_sound, daemon=True).start()
        
        job_type = random.choices(["Metered", "Fixed"], weights = [0.8,0.2])[0]
        start_city = random.choice([
            "Volvo #01-54, London", "POSPED Office #01-12, London", "NBFC, London",
            "SAM BUILDERS, London", "Block 134, London", "TREE-ET, Felixstowe",
            "TradeAUX, Felixstowe", "LKW, Felixstowe", "EuroAcres, Dover",
            "Euro Goodies, Dover", "Ferry Terminal A, Dover", "Eurotunnel Terminal B2", "#01-45, Dover"
        ])
        end_city = random.choice([
            "Volvo #01-54, London", "POSPED Office #01-12, London", "NBFC, London",
            "SAM BUILDERS, London", "Block 134, London", "TREE-ET, Felixstowe",
            "TradeAUX, Felixstowe", "LKW, Felixstowe", "EuroAcres, Dover",
            "Euro Goodies, Dover", "Ferry Terminal A, Dover", "Eurotunnel Terminal B2", "#01-45, Dover"
        ])

        # Ensure start and end are different
        while start_city == end_city:
            end_city = random.choice([
                "Volvo #01-54, London", "POSPED Office #01-12, London", "NBFC, London",
                "SAM BUILDERS, London", "Block 134, London", "TREE-ET, Felixstowe",
                "TradeAUX, Felixstowe", "LKW, Felixstowe", "EuroAcres, Dover",
                "Euro Goodies, Dover", "Ferry Terminal A, Dover", "Eurotunnel Terminal B2", "#01-45, Dover"
            ])

        passenger_name = random.choice([
            "TAN CHENG BOCK", "MUHD SAFFIN BIN OSAM", "LIM PEI PEI", "ONG JUN HAO",
            "NURUL AIN BTE ISMAIL", "ABDULLAH BIN RAZAK", "SIM WEN LI", "GOH WEI HONG"
        ])

        if job_type == "Fixed":
            fare = round(random.uniform(10.00, 100.00), 2)
            self.current_job = {
                "type": "Fixed",
                "passenger": passenger_name,
                "start": start_city,
                "end": end_city,
                "fare": fare
            }
        else:
            self.current_job = {
                "type": "Metered",
                "passenger": passenger_name,
                "start": start_city,
                "end": end_city,
                "fare": 4.40  # Start with flag down fare
            }

        self.show_job_offer()

    def show_job_offer(self):
        self.clear_screen()
        job = self.current_job

        frame = tk.Frame(self, bg="#00008B")
        frame.pack(expand=True)

        title = tk.Label(frame, text="NEW JOB OFFER", font=("Helvetica", 16, "bold"), fg="white", bg="#00008B")
        title.pack(pady=10)

        info = tk.Label(frame, text=f"Passenger: {job['passenger']}\nFrom: {job['start']}\nTo: {job['end']}", font=("Helvetica", 12), fg="white", bg="#00008B")
        info.pack(pady=10)

        if job["type"] == "Fixed":
            fare_label = tk.Label(frame, text=f"Fixed Fare: ${job['fare']:.2f}", font=("Helvetica", 14, "bold"), fg="cyan", bg="#00008B")
            fare_label.pack(pady=5)

        if job["type"] == "Metered":
            fare_label = tk.Label(frame, text=f"Metered Fare ", font=("Helvetica", 14, "bold"), fg="cyan", bg="#00008B")
            fare_label.pack(pady=5)

        button_frame = tk.Frame(frame, bg="#00008B")
        button_frame.pack(pady=15)

        accept_btn = tk.Button(button_frame, text="Accept", width=10, command=self.accept_job)
        accept_btn.grid(row=0, column=0, padx=10)

        decline_btn = tk.Button(button_frame, text="Decline", width=10, command=self.decline_job)
        decline_btn.grid(row=0, column=1, padx=10)

    def accept_job(self):
        self.stop_notification_sound()
        self.start_trip()

    def decline_job(self):
        self.stop_notification_sound()
        self.show_main_menu()
        self.after(500, self.search_for_job)  # Delay a little to let screen reload
       
    def start_trip(self):
        self.clear_screen()
        job = self.current_job
        self.elapsed_start_time = time.time()

        frame = tk.Frame(self, bg="#00008B")
        frame.pack(expand=True)

        trip_title = tk.Label(frame, text="Trip In Progress", font=("Helvetica", 16, "bold"), fg="white", bg="#00008B")
        trip_title.pack(pady=10)

        trip_info = tk.Label(frame, text=f"Passenger: {job['passenger']}\nFrom: {job['start']}\nTo: {job['end']}", font=("Helvetica", 12), fg="white", bg="#00008B")
        trip_info.pack(pady=10)

        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        start_time_info = tk.Label(frame, text=f"Start time: {time_str}", font=("Helvetica", 12), fg="white", bg="#00008B")
        start_time_info.pack(pady=10)

        self.elapsed_time_label = tk.Label(frame, text="Elapsed Time: 0s", font=("Helvetica", 12), fg="white", bg="#00008B")
        self.elapsed_time_label.pack(pady=5)

        self.fare_label = tk.Label(frame, text=f"Fare: ${job['fare']:.2f}", font=("Helvetica", 14, "bold"), fg="cyan", bg="#00008B")
        self.fare_label.pack(pady=5)

        end_trip_btn = tk.Button(frame, text="End Trip", command=self.complete_trip)
        end_trip_btn.pack(pady=20)

        self.update_elapsed()

    def update_elapsed(self):
            if self.elapsed_start_time:
                elapsed = int(time.time() - self.elapsed_start_time)
               
                # Convert to minutes and seconds
                minutes = elapsed // 60
                seconds = elapsed % 60

                if elapsed >= 45:
                    additional_fare = (elapsed // 45) * 0.26
                    self.current_job["fare"] = 4.40 + additional_fare  # Update the fare dynamically
                    self.fare_label.config(text=f"Fare: ${self.current_job['fare']:.2f}")  # Update the displayed fare

                # Format time as MM:SS
                time_str = f"{minutes:02}:{seconds:02}"

                # If the colon is visible, update the label to show the time, else hide the colon
                if self.is_colon_visible:
                    self.elapsed_time_label.config(text=f"{time_str}")
                else:
                    self.elapsed_time_label.config(text=f"{minutes:02}  {seconds:02}")

                # Toggle the visibility of the colon
                self.is_colon_visible = not self.is_colon_visible

                # Update the time every second
                self.after(1000, self.update_elapsed)

    def complete_trip(self):
        if self.current_job:
            self.today_earnings += self.current_job["fare"]
            self.current_job = None
            self.elapsed_start_time = None
            self.show_main_menu()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = TaxiMeterApp()
    app.mainloop()




