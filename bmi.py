import tkinter as tk
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

# ---------- Helper Functions ----------

# Calculate BMI and categorize
def calculate_bmi():
    try:
        # Get inputs
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        
        # Validate reasonable input ranges
        if weight <= 0 or height <= 0 or weight > 300 or height > 3:
            messagebox.showerror("Invalid Input", "Enter realistic weight and height values!")
            return
        
        # Calculate BMI
        bmi = weight / (height ** 2)
        
        # Categorize BMI
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"
        
        # Display BMI result
        result_label.config(text=f"Your BMI: {bmi:.2f}\nCategory: {category}")
        
        # Save data to CSV
        save_bmi_data(bmi, category)
    
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values!")

# Save BMI data to CSV
def save_bmi_data(bmi, category):
    file_exists = os.path.isfile("bmi_history.csv")
    with open("bmi_history.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Weight(kg)", "Height(m)", "BMI", "Category"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                         entry_weight.get(), entry_height.get(), f"{bmi:.2f}", category])

# Visualize BMI history as a graph
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
    
    # Plot graph
    plt.figure(figsize=(8, 4))
    plt.plot(dates, bmis, marker='o', color='green')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Date & Time")
    plt.ylabel("BMI")
    plt.title("BMI History Trend")
    plt.tight_layout()
    plt.show()

# Clear input fields
def clear_inputs():
    entry_weight.delete(0, tk.END)
    entry_height.delete(0, tk.END)
    result_label.config(text="")

# ---------- GUI Design ----------

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x350")
root.config(bg="#f0f0f0")

# Labels & Entries
tk.Label(root, text="Enter Weight (kg):", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
entry_weight = tk.Entry(root, font=("Arial", 12))
entry_weight.pack(pady=5)

tk.Label(root, text="Enter Height (m):", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
entry_height = tk.Entry(root, font=("Arial", 12))
entry_height.pack(pady=5)

# Buttons
tk.Button(root, text="Calculate BMI", command=calculate_bmi, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(root, text="Show BMI History", command=show_bmi_history, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=5)
tk.Button(root, text="Clear", command=clear_inputs, font=("Arial", 12), bg="#f44336", fg="white").pack(pady=5)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0", fg="black")
result_label.pack(pady=10)

root.mainloop()
