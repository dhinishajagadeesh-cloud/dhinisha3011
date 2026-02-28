import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import math
class SmartSheShieldApp:

    def __init__(self, root):
        self.root = root
        self.root.title("🚺 Smart She Shield Tracker")
        self.root.geometry("1000x650")
        self.root.configure(bg="#FAFAFA")

        # Women-based professional theme colors
        self.primary_color = "#C2185B"
        self.secondary_color = "#F3E5F5"
        self.button_color = "#AD1457"

        # Route villages
        self.villages = [
            "Coonoor",
            "Yedapalli",
            "Ellithorai",
            "Bettatai",
            "Naduhatti",
            "Kattabettu",
            "Horasolai",
            "Kotagiri"
        ]

        self.create_home_screen()
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def create_home_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg=self.secondary_color)
        frame.pack(fill="both", expand=True)

        tk.Label(frame,
                 text="SMART SHE SHIELD TRACKER",
                 font=("Helvetica", 24, "bold"),
                 fg=self.primary_color,
                 bg=self.secondary_color).pack(pady=50)

        tk.Label(frame,
                 text="Rural Women Safety Route & Fare Monitoring System",
                 font=("Helvetica", 14),
                 bg=self.secondary_color).pack(pady=10)

        tk.Button(frame,
                  text="Start Monitoring",
                  font=("Helvetica", 14, "bold"),
                  bg=self.button_color,
                  fg="white",
                  padx=25,
                  pady=12,
                  command=self.create_route_screen).pack(pady=30)

    def create_route_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill="both", expand=True)

        tk.Label(frame,
                 text="Travel Details",
                 font=("Helvetica", 20, "bold"),
                 fg=self.primary_color,
                 bg="white").pack(pady=20)

        form = tk.Frame(frame, bg="white")
        form.pack(pady=20)

        tk.Label(form, text="From:", font=("Helvetica", 12),
                 bg="white").grid(row=0, column=0, pady=8, padx=10)
        self.from_box = ttk.Combobox(form, values=self.villages, width=25)
        self.from_box.grid(row=0, column=1)

        tk.Label(form, text="To:", font=("Helvetica", 12),
                 bg="white").grid(row=1, column=0, pady=8, padx=10)
        self.to_box = ttk.Combobox(form, values=self.villages, width=25)
        self.to_box.grid(row=1, column=1)

        tk.Label(form, text="Number of Passengers:",
                 font=("Helvetica", 12),
                 bg="white").grid(row=2, column=0, pady=8, padx=10)
        self.passenger_entry = tk.Entry(form, width=27)
        self.passenger_entry.grid(row=2, column=1)

        tk.Label(form, text="Select Bus Timing:",
                 font=("Helvetica", 12),
                 bg="white").grid(row=3, column=0, pady=8, padx=10)

        self.time_box = ttk.Combobox(form,
                                     values=self.generate_bus_times(),
                                     width=25)
        self.time_box.grid(row=3, column=1)

        tk.Button(frame,
                  text="Check Route",
                  font=("Helvetica", 13, "bold"),
                  bg=self.button_color,
                  fg="white",
                  padx=20,
                  pady=10,
                  command=self.calculate_route).pack(pady=25)

    def create_result_screen(self, result_text):
        self.clear_screen()

        frame = tk.Frame(self.root, bg=self.secondary_color)
        frame.pack(fill="both", expand=True)

        tk.Label(frame,
                 text="Travel Summary",
                 font=("Helvetica", 20, "bold"),
                 fg=self.primary_color,
                 bg=self.secondary_color).pack(pady=20)

        box = tk.Frame(frame, bg="white", bd=2, relief="groove")
        box.pack(padx=80, pady=20)

        text_box = tk.Text(box,
                           width=85,
                           height=18,
                           font=("Helvetica", 12),
                           bg="white")
        text_box.pack(padx=20, pady=20)
        text_box.insert("end", result_text)
        text_box.config(state="disabled")

        tk.Button(frame,
                  text="Back",
                  font=("Helvetica", 12, "bold"),
                  bg=self.button_color,
                  fg="white",
                  command=self.create_route_screen).pack(pady=10)

    def generate_bus_times(self):
        times = []
        start = datetime.strptime("06:00", "%H:%M")
        for i in range(24):
            time = start + timedelta(minutes=30 * i)
            times.append(time.strftime("%I:%M %p"))
        return times

 
    def calculate_distance(self, start_index, end_index):
        total_km = 0
        for i in range(start_index, end_index):
            if i == 0:
                total_km += 14
            elif 1 <= i <= 5:
                total_km += 3
            else:
                total_km += 10
        return total_km

 
    def calculate_time(self, base_time, start_index, end_index):

        departure_time = datetime.strptime(base_time, "%I:%M %p")
        current_time = departure_time
        route_details = ""

        for i in range(start_index, end_index):

            if i == 0:
                current_time += timedelta(minutes=20)
            elif 1 <= i <= 4:
                current_time += timedelta(minutes=7)
            else:
                current_time += timedelta(minutes=10)

            route_details += f"{self.villages[i+1]} - Arrival: {current_time.strftime('%I:%M %p')}\n"

        arrival_time = current_time
        total_minutes = int((arrival_time - departure_time).total_seconds() / 60)

        return (
            departure_time.strftime("%I:%M %p"),
            arrival_time.strftime("%I:%M %p"),
            total_minutes,
            route_details
        )

 
    def calculate_route(self):

        start = self.from_box.get()
        end = self.to_box.get()
        passengers = self.passenger_entry.get()
        base_time = self.time_box.get()

        if not start or not end or not passengers or not base_time:
            messagebox.showerror("Error", "Please fill all fields")
            return

        start_index = self.villages.index(start)
        end_index = self.villages.index(end)

        if start_index >= end_index:
            messagebox.showerror("Error", "Invalid Route Direction")
            return

        passengers = int(passengers)

        distance = self.calculate_distance(start_index, end_index)
        fare = math.ceil(distance * 2.5) * passengers

        departure, arrival, duration, timing_details = self.calculate_time(
            base_time, start_index, end_index
        )

        result = f"""
From: {start}
To: {end}
Passengers: {passengers}

Departure Time : {departure}
Arrival Time   : {arrival}
Total Duration : {duration} Minutes

Total Distance : {distance} km
Total Fare     : ₹{fare}

Stop-by-Stop Timing:
{timing_details}
"""

        self.create_result_screen(result)

root = tk.Tk()
app = SmartSheShieldApp(root)
root.mainloop()