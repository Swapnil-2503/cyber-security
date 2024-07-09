import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

key="key"

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

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.2.2'  # Replace with the actual server IP address
port = 80
client_socket.connect((server_ip, port))

def receive_messages():
    while True:
        try:
            ## decrypt with rc4 same key
            message=rc4(key,client_socket.recv(1024).decode('utf-8'))
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

def set_key_received(event=None):
     global key
     key=symmetric_encryption_key.get()

# Start receiving messages in a separate thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# GUI setup
root = tk.Tk()
root.title("Cyber Security Hacker")
screen_width = 600
screen_height = 600
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, True)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(expand=True, fill=tk.BOTH)

set_label_here=tk.Label(main_frame,text="set key here:")
set_label_here.pack(fill=tk.X,pady=10)

symmetric_encryption_key = ttk.Entry(main_frame)
symmetric_encryption_key.pack(fill=tk.X, pady=10)
symmetric_encryption_key.bind('<Return>', set_key_received)

chat_window = scrolledtext.ScrolledText(main_frame, state=tk.DISABLED)
chat_window.pack(expand=True, fill=tk.BOTH, pady=10)


root.mainloop()
client_socket.close()
