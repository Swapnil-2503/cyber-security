import tkinter as tk
from tkinter import ttk
import socket
import rc4
import RSA
import sDES
import TDES
import hashlib
import threading
import random
import string


ciphertext=""

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8080  # Using a higher port number to avoid potential permission issues

server_ip = '192.168.2.130'  # Bind to all interfaces
server_socket.bind((server_ip, port))
server_socket.listen(5)
print(f"listning on  port 8080 {server_ip}")
clients = []

def accept_clients():
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"Connection from {addr}")

def send_to_client(event=None):
    for client in clients:
        try:
            client.sendall(ciphertext.encode('utf-8'))
            print("send successfully")
        except:
            clients.remove(client)

# Start accepting clients in a separate thread
accept_thread = threading.Thread(target=accept_clients)
accept_thread.daemon = True
accept_thread.start()

# Get the hostname of the local machine
hostname = socket.gethostname()

# Get the IP address corresponding to the hostname
ip_address = socket.gethostbyname(hostname)

print(f"IP Address: {ip_address}")  


# Function to update the second ComboBox based on the first ComboBox selection
def update_combo2(event):
    selected_method = combo1.get()
    if selected_method == "Symmetric Encryption":
        combo2['values'] = ("DES", "TDES","rc4")
    elif selected_method == "Asymmetric Encryption":
        combo2['values'] = ("RSA")
    else:
        combo2['values'] = ()

# Function to handle button clicks
def on_button_click():
    global ciphertext 

    algorithm = combo2.get()
    cryptoType=combo1.get()
    public_key="123456"
    type=True

    if(cryptoType=="Symmetric Encryption"):
        print(public_key)
    else:
        type=False

    plaintext = textarea.get("1.0", tk.END).strip()  # Get and strip the plaintext
    
    md5_key_hash = hashlib.md5(public_key.encode()).hexdigest()  # Hash the key

    if(type==True):

        if algorithm == 'rc4':
            result = hashlib.md5(b'rc4').hexdigest()
            ciphertext = result + "|" + md5_key_hash + "|" + rc4.rc4(plaintext, public_key)

        elif algorithm == 'sDES':
            result = hashlib.md5(b'sDES').hexdigest()
            ciphertext = result + "|" + md5_key_hash + "|" + sDES.sdes_encrypt(plaintext, public_key)

        elif algorithm == 'TDES':
            result = hashlib.md5(b'TDES').hexdigest()
            ciphertext = result + "|" + md5_key_hash + "|" + TDES.tdes_encrypt(plaintext, public_key)

    else:
        if algorithm == 'RSA':
            result = hashlib.md5(b'rc4').hexdigest()
            ciphertext = result + "|" + RSA.rc4(plaintext, public_key)

    print(f"Ciphertext: {ciphertext}")
    send_to_client()



# Create the main window
root = tk.Tk()
root.title(f"Cyber Security Sender ip= {ip_address}")
screen_width = 780
screen_height = 780
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, True)

# Create a frame for layout purposes
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create the first ComboBox
combo_label1 = ttk.Label(frame, text="Choose cryptography method:")
combo_label1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

combo1 = ttk.Combobox(frame)
combo1['values'] = ("Symmetric Encryption", "Asymmetric Encryption")
combo1.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
combo1.bind("<<ComboboxSelected>>", update_combo2)

# Create the second ComboBox
combo_label2 = ttk.Label(frame, text="Choose algorithm:")
combo_label2.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

combo2 = ttk.Combobox(frame)
combo2.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

# Create a TextArea
text_label = ttk.Label(frame, text="Enter text here:")
text_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

textarea = tk.Text(frame, height=10, width=40)
textarea.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

# Create a Button
button = ttk.Button(frame, text="Send message", command=on_button_click)
button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Run the main event loop
root.mainloop()

