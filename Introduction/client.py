import tkinter as tk
from tkinter import ttk, scrolledtext
import socket
import threading
import subprocess
import os
import signal

# Get the hostname and IP address of the local machine
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

commands_executed = []
history_index = -1
current_process = None  # Initialize the current process variable

def connect_to_server_tcp():
    """Attempts to connect to the TCP server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '192.168.223.245'  # Replace with the actual server IP address
    port = 8080
    try:
        client_socket.connect((server_ip, port))
        update_status(f"Connected to TCP server at {server_ip}:{port}")
    except Exception as e:
        update_status(f"Failed to connect to TCP server: {e}")

def connect_to_server_udp():
    """Attempts to connect to the UDP server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ip = '0.0.0.0'  # Replace with the actual server IP address
    port = 8080
    try:
        client_socket.connect((server_ip, port))
        update_status(f"Connected to UDP server at {server_ip}:{port}")
    except Exception as e:
        update_status(f"Failed to connect to UDP server: {e}")

def update_status(message):
    """Updates the status text area with the given message."""
    status_text.config(state=tk.NORMAL)
    status_text.insert(tk.END, message + "\n")
    status_text.config(state=tk.DISABLED)
    status_text.see(tk.END)

def run_command(command):
    """Executes a system command and updates the status text with the output."""
    global current_process
    print(f"Running command: {command}")  # Debugging output
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
    """Handles the Enter key press to execute a command."""
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
    """Handles the Up arrow key to navigate through command history."""
    global history_index
    if commands_executed and history_index > 0:
        history_index -= 1
        command_entry.delete(0, tk.END)
        command_entry.insert(0, f"$ {commands_executed[history_index]}")
        command_entry.icursor(tk.END)

def on_key_down(event):
    """Handles the Down arrow key to navigate through command history."""
    global history_index
    if commands_executed and history_index < len(commands_executed) - 1:
        history_index += 1
        command_entry.delete(0, tk.END)
        command_entry.insert(0, f"$ {commands_executed[history_index]}")
        command_entry.icursor(tk.END)
    elif history_index == len(commands_executed) - 1:
        history_index += 1
        command_entry.delete(0, tk.END)
        command_entry.insert(0, "$ ")
        command_entry.icursor(tk.END)

def interrupt_command():
    """Interrupts the currently running command by sending a SIGINT (Ctrl+C)."""
    global current_process
    if current_process and current_process.poll() is None:  # Check if a process is running
        os.kill(current_process.pid, signal.SIGINT)  # Send Ctrl+C (SIGINT)
        update_status("Command interrupted by user (Ctrl+C).")

# Create the main window
root = tk.Tk()
root.title("Cyber Security Client")
root.geometry("780x780")
root.resizable(False, True)

# Create a frame for layout purposes
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create buttons for TCP and UDP connection
connect_tcp_btn = tk.Button(frame, text="Connect to TCP Server", command=connect_to_server_tcp)
connect_tcp_btn.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

connect_udp_btn = tk.Button(frame, text="Connect to UDP Server", command=connect_to_server_udp)
connect_udp_btn.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

# # Create a button to interrupt a running command
# interrupt_btn = tk.Button(frame, text="Interrupt", command=interrupt_command)
# interrupt_btn.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

command_prompt_label = ttk.Label(frame, text="Type commands:")
command_prompt_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.NSEW)

command_entry = ttk.Entry(frame)
command_entry.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
command_entry.insert(0, "$ ")
command_entry.bind('<Return>', on_command_enter)  # Main Enter key
command_entry.bind('<KP_Enter>', on_command_enter)  # Numpad Enter key
command_entry.bind('<Up>', on_key_up)
command_entry.bind('<Down>', on_key_down)

status_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
status_text.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

# Run the main event loop
root.mainloop()
