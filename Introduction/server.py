import tkinter as tk
from tkinter import ttk,scrolledtext
import socket
import threading

# Server setup
tcp_server_socket = None
udp_server_socket = None
port = 8080  # Using a higher port number to avoid potential permission issues
clients = []

def accept_tcp_clients():
    """Accepts incoming TCP client connections and appends them to the clients list."""
    global tcp_server_socket
    while True:
        try:
            client_socket, addr = tcp_server_socket.accept()
            clients.append(client_socket)
            print(f"TCP Connection from {addr}")
        except Exception as e:
            print(f"Error accepting TCP client: {e}")
            break

def start_tcp_server():
    """Starts the TCP server and begins accepting clients."""
    global tcp_server_socket
    try:
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_socket.bind(('0.0.0.0', port))
        tcp_server_socket.listen(5)
        update_status(f"TCP Server listening on port {port}...")
        
        # Start accepting TCP clients in a separate thread
        accept_thread = threading.Thread(target=accept_tcp_clients, daemon=True)
        accept_thread.start()

        # Print IP Address
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        update_status(f"TCP Server IP Address: {ip_address}")
    except Exception as e:
        update_status(f"Failed to start TCP server: {e}")

def handle_udp_clients():
    """Handles incoming UDP messages."""
    global udp_server_socket
    while True:
        try:
            message, addr = udp_server_socket.recvfrom(1024)  # Buffer size is 1024 bytes
            print(f"UDP Message from {addr}: {message.decode()}")
            update_status(f"UDP Message from {addr}: {message.decode()}")
        except Exception as e:
            print(f"Error receiving UDP message: {e}")
            break

def start_udp_server():
    """Starts the UDP server and begins receiving messages."""
    global udp_server_socket
    try:
        udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server_socket.bind(('0.0.0.0', port))
        update_status(f"UDP Server listening on port {port}...")

        # Start handling UDP messages in a separate thread
        udp_thread = threading.Thread(target=handle_udp_clients, daemon=True)
        udp_thread.start()

        # Print IP Address
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        update_status(f"UDP Server IP Address: {ip_address}")
    except Exception as e:
        update_status(f"Failed to start UDP server: {e}")

def update_status(message):
    """Updates the status text area with the given message."""
    status_text.config(state=tk.NORMAL)
    status_text.insert(tk.END, message + "\n")
    status_text.config(state=tk.DISABLED)
    status_text.see(tk.END)

def stop_server():
    """Stops both TCP and UDP servers and closes all client connections."""
    global tcp_server_socket, udp_server_socket, clients
    try:
        if tcp_server_socket:
            tcp_server_socket.close()
            tcp_server_socket = None
        if udp_server_socket:
            udp_server_socket.close()
            udp_server_socket = None
        for client in clients:
            client.close()
        clients = []
        update_status("Servers stopped.")
    except Exception as e:
        update_status(f"Error stopping servers: {e}")

# Create the main window
root = tk.Tk()
screen_width = 780
screen_height = 780
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, True)
root.title("Server")

# Create a frame for layout purposes
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create buttons for TCP and UDP server actions
tcp_server_create = ttk.Button(frame, text="Start TCP Server", command=start_tcp_server)
tcp_server_create.grid(row=0, column=0, padx=5, pady=5)

udp_server_create = ttk.Button(frame, text="Start UDP Server", command=start_udp_server)
udp_server_create.grid(row=1, column=0, padx=5, pady=5)

stop_server_button = ttk.Button(frame, text="Stop Servers", command=stop_server)
stop_server_button.grid(row=2, column=0, padx=5, pady=5)

# Create a ScrolledText widget to display status messages
status_text = tk.scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
status_text.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

# Run the main event loop
root.mainloop()
