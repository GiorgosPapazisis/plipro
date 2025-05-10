import tkinter as tk
from tkinter import messagebox
import csv
import matplotlib.pyplot as plt
import os

activities = []
weekly_limit = 168
current_user = ""

def update_user_list():
    users = [f[:-4] for f in os.listdir() if f.endswith(".csv")]
    user_menu['menu'].delete(0, 'end')
    for user in users:
        user_menu['menu'].add_command(label=user, command=lambda value=user: select_user(value))

def select_user(username):
    global current_user
    current_user = username
    user_var.set(username)
    load_user_activities()
    messagebox.showinfo("Χρήστης", f"Ορίστηκε ο χρήστης: {current_user}")

def set_user():
    username = user_entry.get().strip()
    if not username:
        messagebox.showwarning("Προσοχή", "Πληκτρολόγησε όνομα χρήστη.")
        return
    select_user(username)
    update_user_list()

def add_activity():
    name = name_entry.get()
    duration = duration_entry.get()
    importance = importance_entry.get()
    category = category_var.get()

    if not current_user:
        messagebox.showerror("Σφάλμα", "Δεν έχει οριστεί χρήστης.")
        return

    if not name or not duration or not importance:
        messagebox.showerror("Σφάλμα", "Συμπλήρωσε όλα τα πεδία!")
        return

    try:
        duration = float(duration)
        importance = int(importance)
    except ValueError:
        messagebox.showerror("Σφάλμα", "Διάρκεια: αριθμός, Σημαντικότητα: ακέραιος")
        return

    activities.append({
        "name": name,
        "duration": duration,
        "importance": importance,
        "category": category
    })

    save_to_csv()
    clear_entries()
    show_activities()

def clear_entries():
    name_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)
    importance_entry.delete(0, tk.END)
    category_var.set("Υποχρέωση")

def show_activities():
    display.delete(1.0, tk.END)
    for act in activities:
        display.insert(tk.END, f"{act['name']} - {act['duration']} ώρες - Σημαντικότητα: {act['importance']} - {act['category']}\n")

def sort_activities():
    sorted_acts = sorted(activities, key=lambda x: x['importance'], reverse=True)
    display.delete(1.0, tk.END)
    total_time = 0
    for act in sorted_acts:
        if total_time + act["duration"] <= weekly_limit:
            total_time += act["duration"]
            display.insert(tk.END, f"[ΕΦΙΚΤΗ] {act['name']} - {act['duration']} ώρες - {act['category']}\n")
        else:
            display.insert(tk.END, f"[ΕΚΤΟΣ ΟΡΙΟΥ] {act['name']} - {act['duration']} ώρες - {act['category']}\n")

def plot_chart():
    feasible_activities = []
    durations = []
    total = 0

    for act in sorted(activities, key=lambda x: x['importance'], reverse=True):
        if total + act["duration"] <= weekly_limit:
            total += act["duration"]
            feasible_activities.append(act["name"])
            durations.append(act["duration"])

    if not feasible_activities:
        messagebox.showinfo("Προσοχή", "Δεν υπάρχουν εφικτές δραστηριότητες για γράφημα!")
        return

    plt.figure(figsize=(10, 6))
    plt.barh(feasible_activities, durations, color='skyblue')
    plt.xlabel("Ώρες")
    plt.title("Κατανομή Χρόνου σε Εφικτές Δραστηριότητες")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def save_to_csv():
    if not current_user:
        return

    filename = f"{current_user}.csv"
    with open(filename, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["name", "duration", "importance", "category"])
        for act in activities:
            writer.writerow([act["name"], act["duration"], act["importance"], act["category"]])

def load_user_activities():
    global activities
    filename = f"{current_user}.csv"
    activities = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                activities.append({
                    "name": row["name"],
                    "duration": float(row["duration"]),
                    "importance": int(row["importance"]),
                    "category": row["category"]
                })
        show_activities()
    except FileNotFoundError:
        activities = []

def remove_activity():
    name_to_remove = remove_entry.get().strip()
    if not name_to_remove:
        messagebox.showwarning("Προσοχή", "Πληκτρολόγησε όνομα για αφαίρεση.")
        return

    global activities
    new_activities = [act for act in activities if act["name"].lower() != name_to_remove.lower()]
    if len(new_activities) == len(activities):
        messagebox.showerror("Σφάλμα", f"Η δραστηριότητα '{name_to_remove}' δεν βρέθηκε.")
        return

    activities = new_activities
    save_to_csv()
    show_activities()
    messagebox.showinfo("Αφαίρεση", f"Η δραστηριότητα '{name_to_remove}' αφαιρέθηκε.")

def calculate_stats():
    obligation_total = 0
    obligation_count = 0
    leisure_total = 0
    leisure_count = 0

    for act in activities:
        if act["category"] == "Υποχρέωση":
            obligation_total += act["duration"]
            obligation_count += 1
        elif act["category"] == "Ελεύθερος χρόνος":
            leisure_total += act["duration"]
            leisure_count += 1

    obligation_avg = obligation_total / obligation_count if obligation_count > 0 else 0
    leisure_avg = leisure_total / leisure_count if leisure_count > 0 else 0

    messagebox.showinfo("Στατιστικά",
        f"Υποχρεώσεις:\n  Σύνολο: {obligation_total:.2f} ώρες\n  Μέσος χρόνος: {obligation_avg:.2f} ώρες\n\n"
        f"Ελεύθερος Χρόνος:\n  Σύνολο: {leisure_total:.2f} ώρες\n  Μέσος χρόνος: {leisure_avg:.2f} ώρες")

# -------------------- GUI SETUP ----------------------
window = tk.Tk()
window.title("Διαχείριση Ελεύθερου Χρόνου")
window.geometry("650x750")

tk.Label(window, text="Όνομα Χρήστη").pack()
user_entry = tk.Entry(window)
user_entry.pack()
tk.Button(window, text="Ορισμός Νέου Χρήστη", command=set_user).pack(pady=2)

tk.Label(window, text="Ή επέλεξε αποθηκευμένο χρήστη").pack()
user_var = tk.StringVar()
user_menu = tk.OptionMenu(window, user_var, "")
user_menu.pack()
update_user_list()

tk.Label(window, text="Όνομα Δραστηριότητας").pack()
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="Διάρκεια (ώρες)").pack()
duration_entry = tk.Entry(window)
duration_entry.pack()

tk.Label(window, text="Σημαντικότητα (1-10)").pack()
importance_entry = tk.Entry(window)
importance_entry.pack()

tk.Label(window, text="Κατηγορία").pack()
category_var = tk.StringVar()
category_var.set("Υποχρέωση")
category_menu = tk.OptionMenu(window, category_var, "Υποχρέωση", "Ελεύθερος χρόνος")
category_menu.pack()

tk.Button(window, text="Προσθήκη", command=add_activity).pack(pady=5)
tk.Button(window, text="Προβολή", command=show_activities).pack(pady=5)
tk.Button(window, text="Ταξινόμηση", command=sort_activities).pack(pady=5)
tk.Button(window, text="Γράφημα", command=plot_chart).pack(pady=5)
tk.Button(window, text="Υπολογισμός Στατιστικών", command=calculate_stats).pack(pady=5)

tk.Label(window, text="Όνομα για Αφαίρεση").pack()
remove_entry = tk.Entry(window)
remove_entry.pack()
tk.Button(window, text="Αφαίρεση", command=remove_activity).pack(pady=5)

display = tk.Text(window, height=15)
display.pack(pady=10)

window.mainloop()