import tkinter as tk
from tkinter import messagebox
import random

class Job:
    def __init__(self, from_city, to_city, transport_type, pay, items):
        self.from_city = from_city
        self.to_city = to_city
        self.transport_type = transport_type
        self.pay = pay
        self.items = items

class JobScreen(tk.Frame):
    def __init__(self, master, back_to_login_callback):
        super().__init__(master)
        self.master = master  # store reference to switch screens
        self.pack(fill="both", expand=True)

        self.back_to_login_callback = back_to_login_callback

        self.cities = ["Spearleaf Refinery", "Shuffleboard Logistics 01", "Shuffleboard Logistics 02", "Fast Automotive Race Track",
                       "Trilobite Gas Station", "Belasco City Garage", "Radio Tower", "Sealbrik Quarry", "Horizon Estate",
                       "Lens Flare Studio", "Hot Rolled Inc. Steel "]
        self.transport_type = "Van"

        self.on_duty = True
        self.current_job = None
        self.job_timer_id = None



        # Job display box frame (orange border)
        self.job_frame = tk.Frame(self, highlightbackground="#FF6600", highlightthickness=3, bd=0)
        self.job_frame.place(x=20, y=70, width=320, height=350)

        # Job info labels
        self.job_from_label = tk.Label(self.job_frame, text="", font=("Arial", 16, "bold"))
        self.job_from_label.pack(pady=(15, 0))

        self.job_to_label = tk.Label(self.job_frame, text="", font=("Arial", 16, "bold"))
        self.job_to_label.pack(pady=(5, 10))

        self.transport_label = tk.Label(self.job_frame, text="", font=("Arial", 14))
        self.transport_label.pack()

        self.items_label = tk.Label(self.job_frame, text="", font=("Arial", 13), fg="black", wraplength=300, justify="center")
        self.items_label.pack(pady=(0, 10))

        self.pay_label = tk.Label(self.job_frame, text="", font=("Arial", 14, "bold"), fg="#FF6600")
        self.pay_label.pack(pady=(10, 15))

        # Accept and Decline buttons
        btn_frame = tk.Frame(self.job_frame)
        btn_frame.pack(pady=(5, 10))

        self.accept_btn = tk.Button(btn_frame, text="Accept", bg="#28a745", fg="white",
                                    font=("Arial", 14, "bold"), width=10, command=self.accept_job)
        self.accept_btn.pack(side="left", padx=10)

        self.decline_btn = tk.Button(btn_frame, text="Decline", bg="#dc3545", fg="white",
                                     font=("Arial", 14, "bold"), width=10, command=self.decline_job)
        self.decline_btn.pack(side="right", padx=10)

        # Logout button (optional)
        self.logout_btn = tk.Button(self, text="Logout", font=("Arial", 12), command=self.logout)
        self.logout_btn.place(x=280, y=10)
        self.start_job_cycle()
        self.clear_job()

    def logout(self):
        self.master.destroy()




    def start_job_cycle(self):
        # Instead of clearing job here, show "Waiting for job..."
        self.job_from_label.config(text="Waiting for next job...")
        self.job_to_label.config(text="")
        self.transport_label.config(text="")
        self.items_label.config(text="")
        self.pay_label.config(text="")
        
        # Disable buttons while waiting for job
        self.accept_btn.config(state="disabled")
        self.decline_btn.config(state="disabled")

        wait_time = random.randint(0, 10) * 1000
        self.job_timer_id = self.after(wait_time, self.assign_job)

    def assign_job(self):
        self.current_job = self.generate_random_job()
        self.show_job(self.current_job)
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

        pay = random.uniform(8, 30)
        pay = f"SGD ${pay:.2f}"

        item_pool = ["Cardboard M", "Cardboard L", "Suitcase", "Bag"]
        num_items = random.randint(1, 3)
        selected_items = random.sample(item_pool, num_items)
        items = [f"{item} x{random.randint(1, 2)}" for item in selected_items]

        return Job(from_city, to_city, self.transport_type, pay, items)

    def show_job(self, job):
        self.job_from_label.config(text=f"From: {job.from_city}")
        self.job_to_label.config(text=f"To: {job.to_city}")
        self.transport_label.config(text=f"Transport: {job.transport_type}")
        self.items_label.config(text="To Collect: " + ", ".join(job.items))
        self.pay_label.config(text=f"Pay: {job.pay}")

    def clear_job(self):
        self.job_from_label.config(text="")
        self.job_to_label.config(text="")
        self.transport_label.config(text="")
        self.items_label.config(text="")
        self.pay_label.config(text="")
        self.accept_btn.config(state="disabled")
        self.decline_btn.config(state="disabled")

    def accept_job(self):
        job = self.current_job  # Save job before clearing
        self.stop_job_cycle()
        self.clear_job()
        self.master.switch_to_job_in_progress(job)



    def decline_job(self):
        self.accept_btn.config(state="disabled")
        self.decline_btn.config(state="disabled")
        self.clear_job()
        self.current_job = None
        if self.on_duty:
            wait_time = random.randint(0, 10) * 1000
            self.job_timer_id = self.after(wait_time, self.assign_job)

import time
from datetime import datetime

class JobInProgressScreen(tk.Frame):
    def __init__(self, master, job, back_callback, accept_time=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.job = job
        self.back_callback = back_callback
        self.start_time = time.time()

        # Use the passed accept_time or fallback to now
        self.accept_time = accept_time if accept_time else time.time()
        accepted_time_str = datetime.fromtimestamp(self.accept_time).strftime("%H:%M:%S")

        tk.Label(self, text="Job In Progress", font=("Arial", 16, "bold")).pack(pady=10)

        info = (
            f"From: {job.from_city}\n"
            f"To: {job.to_city}\n"
            f"Transport: {job.transport_type}\n"
            f"Pay: {job.pay}\n"
            f"Items: {', '.join(job.items)}"
        )
        tk.Label(self, text=info, font=("Arial", 12), justify="left").pack(pady=10)

        # Show accepted time (fixed)
        self.accepted_time_label = tk.Label(self, text=f"Accepted Time: {accepted_time_str}", font=("Arial", 12))
        self.accepted_time_label.pack()

        # Elapsed time
        self.elapsed_label = tk.Label(self, text="", font=("Arial", 12))
        self.elapsed_label.pack()

        self.update_timer()

        # End Job button
        tk.Button(self, text="End Job", bg="#FF6600", fg="white", font=("Arial", 14),
                  command=self.end_job).pack(pady=20)


    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed, 60)
        self.elapsed_label.config(text=f"Elapsed Time: {minutes:02d}:{seconds:02d}")
        self.after(1000, self.update_timer)


    def end_job(self):
        self.back_callback()




class LalamoveDriverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes("-topmost", True)  # <-- always on top
        self.title("Lalamove Driver App")
        self.geometry("360x500")
        self.resizable(False, False)

        self.login_frame = tk.Frame(self)
        self.login_frame.pack(fill="both", expand=True)

        tk.Label(self.login_frame, text="Mobile Number", font=("Arial", 14)).pack(pady=(100,5))
        self.mobile_entry = tk.Entry(self.login_frame, font=("Arial", 16))
        self.mobile_entry.pack(ipadx=50, ipady=8, pady=(0,20))

        tk.Label(self.login_frame, text="Password", font=("Arial", 14)).pack(pady=(0,5))
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 16))
        self.password_entry.pack(ipadx=50, ipady=8, pady=(0,40))

        self.login_button = tk.Button(self.login_frame, text="LOGIN", bg="#FF6600", fg="white",
                                      font=("Arial", 18, "bold"), command=self.login)
        self.login_button.pack(side="bottom", fill="x", ipady=15)

    def switch_to_job_in_progress(self, job):
        accept_time = time.time()
        self.job_screen.pack_forget()
        self.job_progress_screen = JobInProgressScreen(self, job, self.back_to_job_screen, accept_time)


    def back_to_job_screen(self):
        self.job_progress_screen.pack_forget()
        self.job_screen = JobScreen(self, self.back_to_login)


    def login(self):
        mobile = self.mobile_entry.get()
        password = self.password_entry.get()

        if mobile == "1" and password == "1":
            self.open_job_screen()
        else:
            messagebox.showerror("Error", "Invalid mobile number or password.")

    def open_job_screen(self):
        self.login_frame.destroy()
        self.job_screen = JobScreen(self, self.back_to_login)

    def back_to_login(self):
        self.__init__()  # reset the entire window

if __name__ == "__main__":
    app = LalamoveDriverApp()
    app.mainloop()
