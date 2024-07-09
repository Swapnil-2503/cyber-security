import tkinter as tk
from tkinter import ttk, scrolledtext
import socket
import threading


def read_key_from_file(file_path):
    with open(file_path, 'r') as file:
        key = file.read().strip()
    return key

def rc4(key, message):
    global string_out
    S = list(range(256))
    j = 0
    out = []

    # Key Scheduling Algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudorandom Generation Algorithm (PRGA)
    i = j = 0
    for char in message:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(chr(ord(char) ^ K))
    strReturn = ''.join(out)

    return strReturn

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 80  # Using a higher port number to avoid potential permission issues

server_ip = '192.168.2.3'  # Bind to all interfaces
server_socket.bind((server_ip, port))
server_socket.listen(5)
print(f"listning on  port 80 {server_ip}")
clients = []

def accept_clients():
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"Connection from {addr}")

def send_to_client(event=None):
    message = rc4(read_key_from_file('rc4-key.txt'),message_to_client.get())

    message_to_client.delete(0, tk.END)
    for client in clients:
        try:
            client.sendall(message.encode('utf-8'))
        except:
            clients.remove(client)

# Start accepting clients in a separate thread
accept_thread = threading.Thread(target=accept_clients)
accept_thread.daemon = True
accept_thread.start()

# GUI setup
root = tk.Tk()
root.title("Cyber Security Server")
screen_width = 800
screen_height = 800
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, True)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(expand=True, fill=tk.BOTH)

message_to_client = ttk.Entry(main_frame)
message_to_client.pack(fill=tk.X, pady=10)
message_to_client.bind('<Return>', send_to_client)

root.mainloop()
