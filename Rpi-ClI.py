import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading

commands_executed = []
history_index = -1
caps_lock = False  # Initialize Caps Lock state

def update_status(message):
    status_text.config(state=tk.NORMAL)
    status_text.insert(tk.END, message + "\n")
    status_text.config(state=tk.DISABLED)
    status_text.see(tk.END)

def run_command(command):
    global current_process
    current_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    while True:
        output = current_process.stdout.readline()
        if output:
            update_status(output.strip())
        elif current_process.poll() is not None:
            break
    
    stderr_output = current_process.stderr.read()
    if stderr_output:
        update_status(stderr_output.strip())

def on_command_enter(event=None):
    global history_index
    command = command_entry.get().strip('$ ').strip()
    if command:
        update_status(f"$ {command}")
        command_entry.delete(0, tk.END)
        command_entry.insert(0, "$ ")
        commands_executed.append(command)
        history_index = len(commands_executed)
        threading.Thread(target=run_command, args=(command,), daemon=True).start()

def on_key_up(event):
    global history_index
    if commands_executed and history_index > 0:
        history_index -= 1
        command_entry.delete(0, tk.END)
        command_entry.insert(0, f"$ {commands_executed[history_index]}")
        command_entry.icursor(tk.END)  # Move cursor to end of entry

def on_key_down(event):
    global history_index
    if commands_executed and history_index < len(commands_executed) - 1:
        history_index += 1
        command_entry.delete(0, tk.END)
        command_entry.insert(0, f"$ {commands_executed[history_index]}")
        command_entry.icursor(tk.END)  # Move cursor to end of entry
    elif history_index == len(commands_executed) - 1:
        history_index += 1
        command_entry.delete(0, tk.END)
        command_entry.insert(0, "$ ")
        command_entry.icursor(tk.END)  # Move cursor to end of entry

class OnScreenKeyboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '@', '$'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', ':', "'"],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', '\\', '|'],
            ['[', ']', '{', '}', '(', ')', '<', '>', '_', '-', '+', '='],
            ['Caps Lock', 'Enter', 'Space']
        ]
        self.entry = command_entry  # Use the existing command_entry for input

        self.buttons = {}
        for y, row in enumerate(self.keys):
            for x, key in enumerate(row):
                if key == "Space":
                    button = tk.Button(self, text=key, width=10, height=2, command=lambda k=key: self.on_key_press(k))
                elif key == "Caps Lock":
                    button = tk.Button(self, text=key, width=10, height=2, command=self.toggle_caps_lock)
                elif key == "Enter":
                    button = tk.Button(self, text=key, width=10, height=2, command=lambda k=key: self.on_enter_press())
                else:
                    button = tk.Button(self, text=key, width=5, height=2, command=lambda k=key: self.on_key_press(k))
                button.grid(row=y, column=x, padx=2, pady=2)
                self.buttons[key] = button

    def toggle_caps_lock(self):
        global caps_lock
        caps_lock = not caps_lock
        for key in self.buttons:
            if len(key) == 1:  # Only modify alphabetic characters
                if caps_lock:
                    self.buttons[key].config(text=key.upper())
                else:
                    self.buttons[key].config(text=key.lower())

    def on_key_press(self, key):
        if key == "Backspace":
            current_text = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current_text[:-1])
            self.entry.icursor(tk.END)  # Move cursor to end of entry
        elif key == "Space":
            self.entry.insert(tk.END, ' ')
        elif key == "Caps Lock":
            self.toggle_caps_lock()
        else:
            if caps_lock:
                self.entry.insert(tk.END, key.upper())
            else:
                self.entry.insert(tk.END, key.lower())
            self.entry.icursor(tk.END)  # Move cursor to end of entry

    def on_enter_press(self):
        on_command_enter()
        self.entry.icursor(tk.END)  # Move cursor to end of entry

root = tk.Tk()
root.title("Cyber Security Server")
screen_width = 800
screen_height = 800
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, True)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(expand=True, fill=tk.BOTH)

command_prompt_label = ttk.Label(main_frame, text="Type commands:")
command_prompt_label.pack()

command_entry = ttk.Entry(main_frame)
command_entry.pack(fill=tk.X, pady=10)
command_entry.insert(0, "$ ")
command_entry.bind('<Return>', on_command_enter)
command_entry.bind('<Up>', on_key_up)
command_entry.bind('<Down>', on_key_down)

status_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
status_text.pack(fill=tk.BOTH, expand=True)

keyboard_frame = OnScreenKeyboard(root)
keyboard_frame.pack(fill=tk.X, pady=25)

root.mainloop()
