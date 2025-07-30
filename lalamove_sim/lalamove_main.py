import tkinter as tk
import random
import time
from tkinter import messagebox
from datetime import datetime
import json
import os

STATS_FILE = "stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {"deliveries": 0, "phv_jobs": 0, "money_earned": 0.0, "distance_km": 0.0}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

used_names = set()

def generate_singaporean_name():
    chinese_given = [
        "WEI MING", "LI WEI", "JIA HUI", "XIN YI", "ZHEN HAO", "YU TING", "MING YAO", "JUN HUI"
    ]
    malay_given = [
        "MUHAMMAD HAZIQ", "AIMAN SYAH", "NUR FARHANAH", "AISYAH BALQIS", "IRFAN", "NURUL AIN"
    ]
    indian_given = [
        "RAJESH", "SURESH", "DEEPAK", "VISHNU", "PRIYA", "ANITA", "KAVITHA", "RAVI KUMAR"
    ]

    surnames_chinese = ["TAN", "LIM", "LEE", "NG", "GOH", "CHONG"]
    surnames_malay = ["RAHIM", "ISMAIL"]
    surnames_indian = ["KUMAR", "SINGH"]

    ethnic_group = random.choice(["chinese", "malay", "indian"])

    if ethnic_group == "chinese":
        surname = random.choice(surnames_chinese)
        given = random.choice(chinese_given)
    elif ethnic_group == "malay":
        surname = random.choice(surnames_malay)
        given = random.choice(malay_given)
    else:
        surname = random.choice(surnames_indian)
        given = random.choice(indian_given)

    return f"{surname} {given}".upper()

def generate_unique_name():
    while True:
        name = generate_singaporean_name()
        if name not in used_names:
            used_names.add(name)
            return name

class Job:
    def __init__(self, from_city, to_city, transport_type, pay, items, client_name):
        self.from_city = from_city
        self.to_city = to_city
        self.transport_type = transport_type
        self.pay = pay
        self.items = items
        self.client_name = client_name
        self.stats = load_stats()

class JobScreen(tk.Frame):
    def __init__(self, master, driver_mode):
        super().__init__(master)
        self.master = master
        self.driver_mode = driver_mode
        self.configure(bg="#f9f9f9")
        self.pack(fill="both", expand=True)

        self.cities = [
            "Spearleaf Refinery [N]", "Shuffleboard Logistics 01 [C]", "Shuffleboard Logistics 02 [C]",
            "Fast Automotive Race Track [S]", "Trilobite Gas Station [S]", "Belasco City Garage [S]",
            "Radio Tower [S]", "Sealbrik Quarry [S]", "Horizon Estate [C]", "Lens Flare Studio [C]",
            "Hot Rolled Inc. Steel [S-W]"
        ]

        self.transport_type = "Van"
        self.on_duty = True
        self.current_job = None
        self.job_timer_id = None

        # Header Bar
        title_bar = tk.Frame(self, bg="#FF6600")
        title_bar.pack(fill="x", side="top")
        tk.Label(title_bar, text=f"{driver_mode} Mode", font=("Arial", 12, "bold"), bg="#FF6600", fg="white").pack(pady=6)

        btn_top = tk.Frame(self, bg="#f9f9f9")
        btn_top.pack(fill="x", padx=10, pady=4)

        tk.Button(btn_top, text="← Back", font=("Arial", 9), command=self.back_to_mode_selection).pack(side="left")
        tk.Button(btn_top, text="Exit", font=("Arial", 9), command=self.logout).pack(side="right")

        self.job_frame = tk.Frame(self, bg="white", highlightbackground="#FF6600", highlightthickness=2, bd=2)
        self.job_frame.pack(padx=15, pady=10, fill="both", expand=True)

        self.name_label = tk.Label(self.job_frame, font=("Arial", 10, "bold"), bg="white")
        self.name_label.pack(pady=(5, 5))

        self.job_from_label = tk.Label(self.job_frame, font=("Arial", 11, "bold"), bg="white")
        self.job_from_label.pack(pady=(0, 2))

        self.job_to_label = tk.Label(self.job_frame, font=("Arial", 11, "bold"), bg="white")
        self.job_to_label.pack(pady=(0, 8))

        self.transport_label = tk.Label(self.job_frame, font=("Arial", 10), bg="white")
        self.transport_label.pack()

        self.items_label = tk.Label(
            self.job_frame, font=("Arial", 10), bg="white", wraplength=250, justify="center"
        )
        self.items_label.pack(pady=(5, 5))

        self.pay_label = tk.Label(self.job_frame, font=("Arial", 10, "bold"), fg="#FF6600", bg="white")
        self.pay_label.pack(pady=(5, 10))

        btn_frame = tk.Frame(self.job_frame, bg="white")
        btn_frame.pack()

        self.accept_btn = tk.Button(btn_frame, text="Accept", bg="#28a745", fg="white", font=("Arial", 10, "bold"),
                                    width=10, command=self.accept_job)
        self.accept_btn.pack(side="left", padx=(0, 8))

        self.decline_btn = tk.Button(btn_frame, text="Decline", bg="#dc3545", fg="white", font=("Arial", 10, "bold"),
                                     width=10, command=self.decline_job)
        self.decline_btn.pack(side="left")

        self.animate_loading_dots()

        self.start_job_cycle()
        self.clear_job()

    def animate_loading_dots(self, step=0):
        if self.current_job is not None:
            return  # stop animating once a job is assigned
        dots = "." * (step % 4)
        self.job_from_label.config(text=f"Waiting for next job{dots}")
        self.after(500, self.animate_loading_dots, step + 1)
        
    def pulse_button(self, btn, original_bg, highlight="#ffaa00", pulses=2):
        step = 0
        def animate():
            nonlocal step
            if step % 2 == 0:
                btn.config(bg=highlight)
            else:
                btn.config(bg=original_bg)
            step += 1
            if step < pulses * 2:
                self.after(150, animate)
        animate()



class Job:
    def __init__(self, from_city, to_city, transport_type, pay, items, client_name):
        self.from_city = from_city
        self.to_city = to_city
        self.transport_type = transport_type
        self.pay = pay
        self.items = items
        self.client_name = client_name
        self.stats = load_stats()


class JobScreen(tk.Frame):
    def __init__(self, master, driver_mode):
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        self.driver_mode = driver_mode
        self.pack(fill="both", expand=True)

        self.cities = [
            "Spearleaf Refinery [N]", "Shuffleboard Logistics 01 [C]", "Shuffleboard Logistics 02 [C]",
            "Fast Automotive Race Track [S]", "Trilobite Gas Station [S]", "Belasco City Garage [S]",
            "Radio Tower [S]", "Sealbrik Quarry [S]", "Horizon Estate [C]", "Lens Flare Studio [C]",
            "Hot Rolled Inc. Steel [S-W]"
        ]

        self.transport_type = "Car/Van"
        self.on_duty = True
        self.current_job = None
        self.job_timer_id = None

        self.build_ui()
        
    def pulse_button(self, btn, original_bg, highlight="#ffaa00"):
            def down():
                btn.config(bg=highlight)
                self.after(120, up)
            def up():
                btn.config(bg=original_bg)
            down()
    def build_ui(self):
        header = tk.Frame(self, bg="#FF6A00")
        header.pack(fill="x")

        back_btn = tk.Button(header, text="← Back", command=self.back_to_mode_selection,
                             bg="#FF6A00", fg="white", bd=0, font=("Arial", 10, "bold"))
        back_btn.pack(side="left", padx=10, pady=10)

        exit_btn = tk.Button(header, text="Exit", command=self.logout,
                             bg="#FF6A00", fg="white", bd=0, font=("Arial", 10, "bold"))
        exit_btn.pack(side="right", padx=10, pady=10)

        self.job_frame = tk.Frame(self, bg="#F8F8F8", bd=2, relief="groove")
        self.job_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.name_label = tk.Label(self.job_frame, font=("Helvetica", 12, "bold"), bg="#F8F8F8")
        self.name_label.pack(pady=(10, 5))

        self.job_from_label = tk.Label(self.job_frame, font=("Helvetica", 11), bg="#F8F8F8")
        self.job_from_label.pack()

        self.job_to_label = tk.Label(self.job_frame, font=("Helvetica", 11), bg="#F8F8F8")
        self.job_to_label.pack()

        self.transport_label = tk.Label(self.job_frame, font=("Helvetica", 11), bg="#F8F8F8")
        self.transport_label.pack()

        self.items_label = tk.Label(self.job_frame, font=("Helvetica", 10), bg="#F8F8F8", wraplength=220)
        self.items_label.pack(pady=5)

        self.pay_label = tk.Label(self.job_frame, font=("Helvetica", 12, "bold"), fg="#FF6A00", bg="#F8F8F8")
        self.pay_label.pack(pady=5)

        btn_container = tk.Frame(self.job_frame, bg="#F8F8F8")
        btn_container.pack(pady=10)

        self.accept_btn = tk.Button(btn_container, text="Accept", bg="#28A745", fg="white",
                                    font=("Helvetica", 10, "bold"), width=10, command=self.accept_job)
        self.accept_btn = tk.Button(btn_container, text="Accept", bg="#28A745", fg="white",
                            font=("Helvetica", 10, "bold"), width=10, command=self.accept_job)

        self.decline_btn = tk.Button(btn_container, text="Decline", bg="#DC3545", fg="white",
                                     font=("Helvetica", 10, "bold"), width=10, command=self.decline_job)
        self.decline_btn = tk.Button(btn_container, text="Decline", bg="#DC3545", fg="white",
                             font=("Helvetica", 10, "bold"), width=10, command=self.decline_job)

        self.start_job_cycle()
        self.clear_job()

    def logout(self):
        self.master.destroy()

    def start_job_cycle(self):
        self.job_from_label.config(text="Waiting for next job...")
        self.job_to_label.config(text="")
        self.transport_label.config(text="")
        self.items_label.config(text="")
        self.pay_label.config(text="")

        wait_time = random.randint(3, 7) * 1000
        self.job_timer_id = self.after(wait_time, self.assign_job)

    def assign_job(self):
        self.current_job = self.generate_random_job()
        self.show_job(self.current_job)
        self.accept_btn.pack(side="left", padx=10)
        self.decline_btn.pack(side="right", padx=10)
        self.accept_btn.config(state="normal")
        self.decline_btn.config(state="normal")

    def stop_job_cycle(self):
        if self.job_timer_id:
            self.after_cancel(self.job_timer_id)
            self.job_timer_id = None
        self.current_job = None
        self.accept_btn.config(state="disabled")
        self.decline_btn.config(state="disabled")

    def generate_random_job(self):
        from_city = random.choice(self.cities)
        to_city = random.choice(self.cities)
        while to_city == from_city:
            to_city = random.choice(self.cities)

        pay = f"SGD ${random.uniform(8, 30):.2f}"

        if self.driver_mode == "PHV":
            items = []
            if random.random() < 0.2:
                item_pool = ["Suitcase", "Bag"]
                selected_items = random.sample(item_pool, k=random.randint(1, 2))
                items = [f"{item} x{random.randint(1, 2)}" for item in selected_items]
        else:  # Delivery
            item_pool = ["Cardboard M", "Cardboard L", "Suitcase", "Bag"]
            selected_items = random.sample(item_pool, k=random.randint(1, 3))
            items = [f"{item} x{random.randint(1, 2)}" for item in selected_items]

        client_name = generate_unique_name()
        return Job(from_city, to_city, self.transport_type, pay, items, client_name)

    def show_job(self, job):
        self.name_label.config(text=f"👤 Customer: {job.client_name}")
        self.job_from_label.config(text=f"📍 From: {job.from_city}")
        self.job_to_label.config(text=f"📍 To: {job.to_city}")
        self.transport_label.config(text=f"🚗 Transport: {job.transport_type}")

        item_text = "📦 Items: " + ", ".join(job.items) if job.items else "📦 Items: None"
        self.items_label.config(text=item_text)

        self.pay_label.config(text=f"💰 {job.pay}")

    def clear_job(self):
        self.name_label.config(text="")
        self.job_from_label.config(text="")
        self.job_to_label.config(text="")
        self.transport_label.config(text="")
        self.items_label.config(text="")
        self.pay_label.config(text="")

        self.accept_btn.config(state="disabled")
        self.decline_btn.config(state="disabled")
    
        # Add this:
        self.accept_btn.pack_forget()
        self.decline_btn.pack_forget()

    def accept_job(self):
        self.pulse_button(self.accept_btn, "#28a745")
        job = self.current_job
        self.stop_job_cycle()
        self.clear_job()
        self.master.switch_to_job_in_progress(job)

    def decline_job(self):
        self.pulse_button(self.decline_btn, "#dc3545")
        self.accept_btn.config(state="disabled")
        self.decline_btn.config(state="disabled")
        self.clear_job()
        self.current_job = None
        if self.on_duty:
            wait_time = random.randint(3, 7) * 1000
            self.job_timer_id = self.after(wait_time, self.assign_job)

    def back_to_mode_selection(self):
        self.pack_forget()
        self.master.ask_driver_mode()


class JobInProgressScreen(tk.Frame):
    def __init__(self, master, job, back_callback):
        super().__init__(master)
        self.master = master
        self.job = job
        self.back_callback = back_callback
        self.start_time = time.time()
        self.arrived = False
        self.second_stage_started = False
        self.arrive_minutes = random.randint(5, 7)
        self.trip_minutes = random.randint(5, 10)

        self.configure(bg="#ffffff")
        self.pack(fill="both", expand=True)

        tk.Label(self, text="🚗 Job In Progress", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=15)

        job_info = (
            f"👤 Passenger: {job.client_name}\n"
            f"📍 From: {job.from_city}\n"
            f"📍 To: {job.to_city}\n"
            f"🚗 Transport: {job.transport_type}\n"
            f"💰 Pay: {job.pay}\n"
            f"📦 Items: {', '.join(job.items) if job.items else 'None'}"
        )

        tk.Label(self, text=job_info, font=("Arial", 12), bg="#ffffff", justify="left").pack(pady=5)

        self.accepted_time_label = tk.Label(self, text=f"⏱ Accepted Time: {self._time_now()}",
                                            font=("Arial", 12), bg="#ffffff")
        self.accepted_time_label.pack(pady=5)

        self.status_label = tk.Label(self, text=f"📍 Arrive in: {self.arrive_minutes} min",
                                     font=("Arial", 12), bg="#ffffff")
        self.status_label.pack(pady=5)

        self.elapsed_label = tk.Label(self, text="", font=("Arial", 12), bg="#ffffff")
        self.elapsed_label.pack(pady=5)

        self.action_btn = tk.Button(self, text="Arrived", bg="#007bff", fg="white",
                                    font=("Arial", 12, "bold"), width=15, command=self.arrived_pressed)
        self.action_btn.pack(pady=15)

        self.update_timer()

    def _time_now(self):
        return datetime.now().strftime("%H:%M:%S")

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed, 60)

        if not self.arrived:
            remaining = max(0, self.arrive_minutes * 60 - elapsed)
            mins, secs = divmod(remaining, 60)
            self.status_label.config(text=f"📍 Arrive in: {mins}m {secs}s")
        elif self.second_stage_started:
            remaining = max(0, self.trip_minutes * 60 - (elapsed - self.arrive_time))
            mins, secs = divmod(remaining, 60)
            self.status_label.config(text=f"🚘 Trip in Progress: {mins}m {secs}s")

        self.elapsed_label.config(text=f"🕒 Elapsed Time: {minutes:02d}:{seconds:02d}")
        self.after(1000, self.update_timer)

    def arrived_pressed(self):
        if not self.arrived:
            self.arrived = True
            self.arrive_time = int(time.time() - self.start_time)
            self.accepted_time_label.config(text=f"✅ Arrived Time: {self._time_now()}")
            self.action_btn.config(text="End Job", command=self.end_job, bg="#28a745")
            self.second_stage_started = True
        else:
            self.end_job()

    def end_job(self):
        app = self.master
        job = self.job
        stats = app.stats

        if app.driver_mode == "Delivery":
            stats["deliveries"] += 1
        else:
            stats["phv_jobs"] += 1

        try:
            amount = float(job.pay.replace("SGD $", ""))
            stats["money_earned"] += amount
        except:
            pass

        stats["distance_km"] += 0.0  # Placeholder

        save_stats(stats)
        self.back_callback()


class LalamoveDriverApp(tk.Tk):
    def __init__(self):
        
        super().__init__()
        self.title("Driver App")
        self.geometry("260x360")
        self.resizable(False, False)
        self.configure(bg="#f2f2f2")
        self.stats = load_stats()
        self.driver_mode = None
        self.wm_attributes("-topmost", 1)
        
        try:
            self.iconbitmap("icon.ico")
        except:
            pass

        self.ask_driver_mode()

    def ask_driver_mode(self):
        self.clear_window()

        frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="c", width=280, height=330)

        tk.Label(frame, text="🛵 Select Driver Type", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=20)

        tk.Button(frame, text="📦 Delivery Driver", font=("Arial", 12), width=22,
                  bg="#FFCC00", command=lambda: self.set_driver_mode("Delivery")).pack(pady=5)

        tk.Button(frame, text="🚘 PHV Driver", font=("Arial", 12), width=22,
                  bg="#00ccff", command=lambda: self.set_driver_mode("PHV")).pack(pady=5)

        tk.Button(frame, text="📊 View Stats", font=("Arial", 12), width=22,
                  command=self.open_stats_screen).pack(pady=5)

        tk.Button(frame, text="❌ Exit", font=("Arial", 10), command=self.destroy).pack(pady=15)

        self.mode_frame = frame

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def set_driver_mode(self, mode):
        def _go():
            self.driver_mode = mode
            self.mode_frame.destroy()
            self.open_job_screen()
        _go()

    def open_job_screen(self):
        if hasattr(self, "job_screen"):
            self.job_screen.destroy()
        self.job_screen = JobScreen(self, self.driver_mode)

    def switch_to_job_in_progress(self, job):
        self.job_screen.pack_forget()
        self.job_progress_screen = JobInProgressScreen(self, job, self.back_to_job_screen)

    def back_to_job_screen(self):
        def _go():
            if hasattr(self, "job_progress_screen"):
                self.job_progress_screen.destroy()
            self.open_job_screen()
        _go()


    def open_stats_screen(self):
        def _go():
            self.clear_window()
            self.stats_screen = StatsScreen(self, self.ask_driver_mode)
        _go()

class StatsScreen(tk.Frame):
    def __init__(self, master, back_callback):
        super().__init__(master)
        self.master = master
        self.back_callback = back_callback
        self.configure(bg="#ffffff")
        self.pack(fill="both", expand=True)

        tk.Label(self, text="📊 Driver Stats", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=20)

        stats = load_stats()
        stat_text = (
            f"📦 Deliveries Completed: {stats['deliveries']}\n"
            f"🚘 PHV Jobs Completed: {stats['phv_jobs']}\n"
            f"💰 Total Earned: SGD ${stats['money_earned']:.2f}\n"
            f"📍 Distance Travelled: {stats['distance_km']:.2f} km"
        )

        tk.Label(self, text=stat_text, font=("Arial", 12), bg="#ffffff", justify="left").pack(pady=10)

        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.pack(side="bottom", pady=15)

        tk.Button(btn_frame, text="← Back", font=("Arial", 11), width=10,
                  command=self.back_callback).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Exit", font=("Arial", 11), width=10,
                  command=self.master.destroy).pack(side="right", padx=20)

if __name__ == "__main__":
    app = LalamoveDriverApp()
    app.mainloop()
