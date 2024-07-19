import tkinter as tk
from tkinter import ttk
import socket
import socket
import rc4
import RSA
import sDES
import TDES
import threading
import hashlib
import random


# Get the hostname of the local machine
hostname = socket.gethostname()
# Get the IP address corresponding to the hostname
ip_address = socket.gethostbyname(hostname)
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.2.130'  # Replace with the actual server IP address
port = 8080
client_socket.connect((server_ip, port))



def received_Messages(ciphertext):
    hash_and_message = ciphertext.split('|')
    received_hash = hash_and_message[0]
    received_key_hash = hash_and_message[1]
    encrypted_message = hash_and_message[2]
    
    print(f"Encrypted text: {encrypted_message}")

    # Calculate MD5 hashes for each algorithm
    hash_rc4 = hashlib.md5(b'rc4').hexdigest()
    hash_RSA = hashlib.md5(b'RSA').hexdigest()
    hash_sDES = hashlib.md5(b'sDES').hexdigest()
    hash_TDES = hashlib.md5(b'TDES').hexdigest()

    # Compare received hash with computed hashes to identify the algorithm
    if received_hash == hash_rc4:
        identified_algorithm = 'rc4'
    elif received_hash == hash_RSA:
        identified_algorithm = 'RSA'
    elif received_hash == hash_sDES:
        identified_algorithm = 'sDES'
    elif received_hash == hash_TDES:
        identified_algorithm = 'TDES'
    else:
        identified_algorithm = 'Unknown'

    print(f"Identified Algorithm: {identified_algorithm}")
    print(f"Received Key Hash: {received_key_hash}")
    md5_key_hash = hashlib.md5("123456".encode()).hexdigest()
    key=""
    plaintext=""
    
    if(md5_key_hash==received_key_hash):
        key="123456"

    if(identified_algorithm=="rc4"):
        plaintext=rc4.rc4(encrypted_message,key)
    print(f"key:{key} plaintext : {plaintext}")
    return plaintext


def receive_messages():
    while True:
        try:
            ## decrypt with rc4 same key
            message_received=client_socket.recv(1024).decode('utf-8')
            plaintext=received_Messages(message_received)
            if plaintext:
                print(f"Server: {plaintext}")  # Print the message to the console
                received_textarea.config(state=tk.NORMAL)
                received_textarea.insert(tk.END, f"Sender: {plaintext}\n")
                received_textarea.config(state=tk.DISABLED)
                received_textarea.yview(tk.END)
            else:
                break
        except:
            break
        
accept_thread = threading.Thread(target=receive_messages)
accept_thread.daemon = True
accept_thread.start()


# Create the main window
root = tk.Tk()
root.title(f"Cyber Security Receiver ip={ip_address}")
screen_width = 780
screen_height = 780
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, True)

# Create a frame for layout purposes
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Create a TextArea for received messages
received_label = ttk.Label(frame, text="Received messages from server:")
received_label.pack(fill=tk.X, padx=5, pady=5)

received_textarea = tk.Text(frame, height=10, width=40)
received_textarea.pack(fill=tk.X, padx=5, pady=5)

# Run the main event loop
root.mainloop()