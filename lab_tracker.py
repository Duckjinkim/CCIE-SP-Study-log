import tkinter as tk
from datetime import datetime, timedelta
import os
import subprocess

# ===== Configuration (CCIE SP) =====
TRACK_NAME = "CCIE SP"                 # Certification track shown in UI / logs
REPO_DIR = r"Z:\CCIE EI\CCIE SP\CCIE-SP-Study-Log"   # Local git repo folder
LOG_FILENAME = "CCIE-SP-Study-log.txt"               # Log file name inside repo
GIT_BRANCH = "main"                    # New GitHub repos default to 'main'
LAB_HOURS = 5                          # Lab length in hours
NUM_SECTIONS = 6                       # Number of lab sections
# ===================================

# Global variables
start_time = None
timer_running = False
paused = False
remaining_time = timedelta(hours=LAB_HOURS)  # Start from LAB_HOURS
last_start_time = None
section_times = {f"Section {i}": None for i in range(1, NUM_SECTIONS + 1)}  # Completion time for each section
section_labels = {}  # Labels for section times

# Log file path
log_file = os.path.join(REPO_DIR, LOG_FILENAME)

# Make sure log directory exists
log_dir = os.path.dirname(log_file)
os.makedirs(log_dir, exist_ok=True)
print(f"[DEBUG] log_file set to: {log_file}")
print(f"[DEBUG] log_dir exists: {os.path.exists(log_dir)}")

def update_timer():
    """Update remaining time using Tkinter's event loop"""
    global remaining_time, last_start_time, timer_running
    if timer_running and last_start_time and not paused:
        elapsed = datetime.now() - last_start_time
        current_remaining = remaining_time - elapsed
        if current_remaining.total_seconds() <= 0:
            remaining_time = timedelta(seconds=0)
            elapsed_time_label.config(text="Time Remaining: 00:00:00")
            timer_running = False
            auto_exit()
            return
        hours, remainder = divmod(int(current_remaining.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        elapsed_time_label.config(text=f"Time Remaining: {time_str}")
    if timer_running:
        window.after(1000, update_timer)

def start_lab():
    """Start or resume the lab"""
    global start_time, last_start_time, timer_running, paused, remaining_time
    if not timer_running:
        if paused:
            last_start_time = datetime.now()
        else:
            start_time = datetime.now()
            last_start_time = start_time
            remaining_time = timedelta(hours=LAB_HOURS)
        status_label.config(text=f"Lab Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}", fg="#00ff00")
        timer_running = True
        paused = False
        update_timer()

def stop_lab():
    """Pause the lab"""
    global remaining_time, last_start_time, timer_running, paused
    if not last_start_time:
        status_label.config(text="Please start the lab first!", fg="#ff0000")
        return
    elapsed = datetime.now() - last_start_time
    remaining_time -= elapsed
    last_start_time = None
    timer_running = False
    paused = True
    status_label.config(text="Lab Paused", fg="#ffcc00")

def section_checked(section):
    """Record time for the selected section"""
    global remaining_time, last_start_time
    if not last_start_time and not paused:
        status_label.config(text="Please start the lab first!", fg="#ff0000")
        return
    current_remaining = remaining_time
    if last_start_time:
        elapsed = datetime.now() - last_start_time
        current_remaining -= elapsed
    hours, remainder = divmod(int(current_remaining.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    section_times[section] = elapsed_str
    section_labels[section].config(text=f"{section}: {elapsed_str}")

def auto_exit():
    """Auto-exit when time reaches 0 and save to GitHub"""
    global timer_running, start_time, paused
    timer_running = False
    if start_time is None:
        start_time = datetime.now()
    log_entry = f"{start_time.strftime('%Y-%m-%d')}: {LAB_HOURS:.2f} hours - {TRACK_NAME} Lab (Completed)\n"
    log_entry += "Section Times:\n"
    for section, time in section_times.items():
        if time:
            log_entry += f"  {section}: {time}\n"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        commit_and_push(log_entry)
        status_label.config(text="Time's up! Please start a new lab.", fg="#ff0000")
    except Exception as e:
        status_label.config(text=f"Log file error: {e}", fg="#ff0000")
    start_time = None
    last_start_time = None
    paused = False
    for section in section_times:
        section_times[section] = None
        section_labels[section].config(text=f"{section}: --:--:--")

def exit_app():
    """Exit the app and save records to GitHub"""
    global remaining_time, last_start_time, timer_running, start_time
    timer_running = False
    if start_time is None:
        start_time = datetime.now()
    if last_start_time:
        elapsed = datetime.now() - last_start_time
        remaining_time -= elapsed
    hours_spent = (timedelta(hours=LAB_HOURS) - remaining_time).total_seconds() / 3600
    log_entry = f"{start_time.strftime('%Y-%m-%d')}: {hours_spent:.2f} hours - {TRACK_NAME} Lab\n"
    log_entry += "Section Times:\n"
    for section, time in section_times.items():
        if time:
            log_entry += f"  {section}: {time}\n"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        commit_and_push(log_entry)
    except Exception as e:
        status_label.config(text=f"Log file error: {e}", fg="#ff0000")
    window.destroy()

def commit_and_push(log_entry):
    """Commit and push to GitHub with error handling"""
    try:
        os.chdir(REPO_DIR)
        subprocess.run(["git", "add", LOG_FILENAME], check=True)
        subprocess.run(["git", "commit", "-m", f"Lab Record: {log_entry.splitlines()[0]}"], check=True)
        subprocess.run(["git", "push", "origin", GIT_BRANCH], check=True)
        status_label.config(text="Successfully pushed to GitHub!", fg="#00ff00")
    except subprocess.CalledProcessError as e:
        status_label.config(text=f"Git error: {e}", fg="#ff0000")
    except Exception as e:
        status_label.config(text=f"Unexpected error: {e}", fg="#ff0000")

# GUI creation
window = tk.Tk()
window.title(f"{TRACK_NAME} Study LAB Time")
window.geometry("800x600")
window.configure(bg="#1e1e2f")
window.resizable(True, True)

main_frame = tk.Frame(window, bg="#1e1e2f")
main_frame.pack(fill="both", expand=True)

elapsed_time_label = tk.Label(main_frame, text=f"Time Remaining: {LAB_HOURS:02d}:00:00", font=("Arial", 35, "bold"), fg="#ff0000", bg="#1e1e2f", highlightbackground="#ff0000", highlightthickness=2)
elapsed_time_label.pack(pady=5)

title_label = tk.Label(main_frame, text=f"{TRACK_NAME} Study LAB Time", font=("Arial", 30, "bold"), fg="#00b7eb", bg="#1e1e2f")
title_label.pack(pady=5)

status_label = tk.Label(main_frame, text="Start the Lab!", font=("Arial", 16), fg="#ffffff", bg="#1e1e2f")
status_label.pack(pady=10)

section_frame = tk.Frame(main_frame, bg="#1e1e2f")
section_frame.pack(pady=10)

rows_per_col = (NUM_SECTIONS + 1) // 2
for i in range(1, NUM_SECTIONS + 1):
    section = f"Section {i}"
    var = tk.BooleanVar()
    col = 0 if i <= rows_per_col else 1
    row = (i - 1) % rows_per_col
    chk = tk.Checkbutton(section_frame, text=section, variable=var, command=lambda s=section: section_checked(s), font=("Arial", 14), fg="#ffffff", bg="#1e1e2f", selectcolor="#1e1e2f")
    chk.grid(row=row*2, column=col, padx=20, pady=5)
    time_label = tk.Label(section_frame, text=f"{section}: --:--:--", font=("Arial", 12), fg="#ffcc00", bg="#1e1e2f")
    time_label.grid(row=row*2+1, column=col, padx=20, pady=5)
    section_labels[section] = time_label

button_frame = tk.Frame(main_frame, bg="#1e1e2f")
button_frame.pack(pady=20)

button_style = {"font": ("Arial", 14, "bold"), "width": 10, "height": 3, "bd": 2, "relief": "raised", "borderwidth": 3}

start_button = tk.Button(button_frame, text="Start", command=start_lab, bg="#4caf50", fg="white", **button_style)
start_button.grid(row=0, column=0, padx=20)

stop_button = tk.Button(button_frame, text="Stop", command=stop_lab, bg="#f44336", fg="white", **button_style)
stop_button.grid(row=0, column=1, padx=20)

exit_button = tk.Button(button_frame, text="Exit", command=exit_app, bg="#607d8b", fg="white", **button_style)
exit_button.grid(row=0, column=2, padx=20)

window.mainloop()
