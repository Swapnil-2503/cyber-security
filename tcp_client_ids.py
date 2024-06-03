import socket

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
