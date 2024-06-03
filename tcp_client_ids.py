import socket

# Define server details
server_host = '192.168.2.5'  # Replace with the actual IP address of the Windows server
server_port = 9999

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((server_host, server_port))
    print(f"Connected to server at {server_host}:{server_port}")

    # Send data to the server
    message = "Hello, World!"
    client_socket.sendall(message.encode())
    print(f"Sent '{message}' to the server")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the client socket
    client_socket.close()
