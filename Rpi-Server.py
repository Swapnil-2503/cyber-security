import tkinter as tk
from tkinter import ttk
import subprocess
import threading

def update_status(message):
    status_text.config(state=tk.NORMAL)
    status_text.insert(tk.END, message + "\n")
    status_text.config(state=tk.DISABLED)
    status_text.see(tk.END)

def on_start_button():
    threading.Thread(target=start_server, daemon=True).start()

def run_command(command):
    try:
        # Use subprocess to run the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        return output
    except Exception as e:
        return str(e)

def on_command_enter(event=None):
    command = command_entry.get().strip('$ ').strip()
    if command:
        update_status(f"$ {command}")
        output = run_command(command)
        update_status(output)
        command_entry.delete(0, tk.END)
        command_entry.insert(0, "$ ")

root = tk.Tk()
root.title("Cyber Security Server")
screen_width = 780
screen_height = 780
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, True)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(expand=True, fill=tk.BOTH)

command_prompt_label = ttk.Label(main_frame, text="Type commands:")
command_prompt_label.pack()

command_entry = ttk.Entry(main_frame)
command_entry.pack(fill=tk.X)
command_entry.insert(0, "$ ")
command_entry.bind('<Return>', on_command_enter)

status_text = tk.Text(main_frame, wrap=tk.WORD, state=tk.DISABLED, height=20)
status_text.pack(fill=tk.BOTH)

root.mainloop()
