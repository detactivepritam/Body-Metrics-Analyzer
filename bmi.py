import tkinter as tk
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

PRIMARY_BG = "#222831"
SECONDARY_BG = "#393E46"
ACCENT = "#00ADB5"
BUTTON_BG = "#00ADB5"
BUTTON_FG = "#EEEEEE"
LABEL_FG = "#EEEEEE"
ENTRY_BG = "#393E46"
ENTRY_FG = "#FFFFFF"
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_LABEL = ("Segoe UI", 12)
FONT_RESULT = ("Segoe UI", 14, "bold")

def calculate_bmi():
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        if weight <= 0 or height <= 0 or weight > 300 or height > 3:
            messagebox.showerror("Invalid Input", "Enter realistic weight and height values!")
            return
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"
        result_label.config(
            text=f"Your BMI: {bmi:.2f}\nCategory: {category}",
            fg=ACCENT
        )
        save_bmi_data(bmi, category)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values!")

def save_bmi_data(bmi, category):
    file_exists = os.path.isfile("bmi_history.csv")
    with open("bmi_history.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Weight(kg)", "Height(m)", "BMI", "Category"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         entry_weight.get(), entry_height.get(), f"{bmi:.2f}", category])

def show_bmi_history():
    if not os.path.exists("bmi_history.csv"):
        messagebox.showinfo("No Data", "No BMI history available yet!")
        return
    dates, bmis = [], []
    with open("bmi_history.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row["Date"])
            bmis.append(float(row["BMI"]))
    plt.figure(figsize=(8, 4))
    plt.plot(dates, bmis, marker='o', color=ACCENT)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Date & Time")
    plt.ylabel("BMI")
    plt.title("BMI History Trend")
    plt.tight_layout()
    plt.show()

def clear_inputs():
    entry_weight.delete(0, tk.END)
    entry_height.delete(0, tk.END)
    result_label.config(text="")

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("420x400")
root.config(bg=PRIMARY_BG)
root.resizable(False, False)

main_frame = tk.Frame(root, bg=SECONDARY_BG, bd=2, relief=tk.RIDGE)
main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380, height=360)

title = tk.Label(main_frame, text="BMI Calculator", font=FONT_TITLE, bg=SECONDARY_BG, fg=ACCENT)
title.pack(pady=(18, 10))

label_weight = tk.Label(main_frame, text="Weight (kg):", font=FONT_LABEL, bg=SECONDARY_BG, fg=LABEL_FG)
label_weight.pack(anchor="w", padx=30, pady=(10, 2))
entry_weight = tk.Entry(main_frame, font=FONT_LABEL, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG, relief=tk.FLAT)
entry_weight.pack(fill="x", padx=30, pady=(0, 8))

label_height = tk.Label(main_frame, text="Height (m):", font=FONT_LABEL, bg=SECONDARY_BG, fg=LABEL_FG)
label_height.pack(anchor="w", padx=30, pady=(0, 2))
entry_height = tk.Entry(main_frame, font=FONT_LABEL, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG, relief=tk.FLAT)
entry_height.pack(fill="x", padx=30, pady=(0, 12))

btn_frame = tk.Frame(main_frame, bg=SECONDARY_BG)
btn_frame.pack(pady=8)

btn_calc = tk.Button(btn_frame, text="Calculate BMI", command=calculate_bmi, font=FONT_LABEL,
                     bg=BUTTON_BG, fg=BUTTON_FG, activebackground=ACCENT, activeforeground=LABEL_FG, width=14, relief=tk.FLAT)
btn_calc.grid(row=0, column=0, padx=5)

btn_history = tk.Button(btn_frame, text="Show History", command=show_bmi_history, font=FONT_LABEL,
                        bg="#222831", fg=ACCENT, activebackground=ACCENT, activeforeground=LABEL_FG, width=12, relief=tk.FLAT)
btn_history.grid(row=0, column=1, padx=5)

btn_clear = tk.Button(btn_frame, text="Clear", command=clear_inputs, font=FONT_LABEL,
                      bg="#393E46", fg="#EEEEEE", activebackground=ACCENT, activeforeground=LABEL_FG, width=8, relief=tk.FLAT)
btn_clear.grid(row=0, column=2, padx=5)

result_label = tk.Label(main_frame, text="", font=FONT_RESULT, bg=SECONDARY_BG, fg=ACCENT, wraplength=320, justify="center")
result_label.pack(pady=(18, 0))

root.mainloop()