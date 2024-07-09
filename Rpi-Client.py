import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.2.2'  # Replace with the actual server IP address
port = 80
client_socket.connect((server_ip, port))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Server: {message}")  # Print the message to the console
                chat_window.config(state=tk.NORMAL)
                chat_window.insert(tk.END, f"Server: {message}\n")
                chat_window.config(state=tk.DISABLED)
                chat_window.yview(tk.END)
            else:
                break
        except:
            break

def send_to_server(event=None):
    message = message_to_server.get()
    message_to_server.delete(0, tk.END)
    client_socket.sendall(message.encode('utf-8'))

# Start receiving messages in a separate thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# GUI setup
root = tk.Tk()
root.title("Cyber Security Client")
screen_width = 800
screen_height = 800
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, True)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(expand=True, fill=tk.BOTH)

chat_window = scrolledtext.ScrolledText(main_frame, state=tk.DISABLED)
chat_window.pack(expand=True, fill=tk.BOTH, pady=10)

message_to_server = ttk.Entry(main_frame)
message_to_server.pack(fill=tk.X, pady=10)
message_to_server.bind('<Return>', send_to_server)

root.mainloop()
client_socket.close()
