import socket
from scapy.all import sniff, IP, TCP

# Define server details
server_host = 'windows_server_ip'  # Replace with the actual IP address of the Windows server
server_port = 9999

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_host, server_port))

# Send data to the server
message = "Hello, Server"
client_socket.sendall(message.encode())

# Receive data from the server
response = client_socket.recv(1024)
print(f"Received '{response.decode()}' from the server")

# Close the client socket
client_socket.close()

# Define a packet callback function for IDS
def packet_callback(packet):
    if packet.haslayer(TCP) and packet[IP].dst == server_host and packet[TCP].dport == server_port:
        print(f"Captured packet: {packet.summary()}")

# Start sniffing traffic
print(f"Starting IDS to monitor traffic to {server_host}:{server_port}")
sniff(filter=f"tcp and dst host {server_host} and dst port {server_port}", prn=packet_callback, store=0)
