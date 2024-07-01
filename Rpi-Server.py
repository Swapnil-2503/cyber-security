import tkinter as tk
from tkinter import ttk
import socket
import threading
import subprocess

def get_local_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        return None

def start_server():
    global server_socket
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((get_local_ip_address(), 9999))
    except Exception as e:
        update_status(f"Failed to bind socket: {e}")
        return

    server_socket.listen(5)
    update_status("Server listening on port 9999")

    try:
        while True:
            # Accept a connection
            client_socket, addr = server_socket.accept()
            update_status(f"Got a connection from {addr}")

            # Receive data from the client
            data = client_socket.recv(1024).decode()
            if not data:
                break
            update_status(f"Received '{data}' from the client")

            # Send a response back to the client
            response = "Echo: " + data
            client_socket.sendall(response.encode())
            update_status(f"Sent '{response}' to the client")

            # Close the client socket
            client_socket.close()

    except Exception as e:
        update_status(f"Server error: {e}")
    finally:
        # Close the server socket
        server_socket.close()

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

# start_button = ttk.Button(main_frame, text="Start Server", command=on_start_button)
# start_button.pack()

root.mainloop()
