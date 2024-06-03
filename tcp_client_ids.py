import socket
import subprocess
import RPi.GPIO as GPIO
import time

# GPIO pin for IR sensor
IR_PIN = 17

# Define server details
server_host = '192.168.2.5'  # Replace with the actual IP address of the Windows server
server_port = 9999

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IDS rule: Example regular expression to detect SQL injection attempt
sql_injection_pattern = re.compile(r'\b(SELECT|UPDATE|DELETE|INSERT|DROP|UNION)\b', re.IGNORECASE)

def monitor_ir_sensor():
    # Monitor IR sensor for object detection
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(IR_PIN, GPIO.IN)

        while True:
            if GPIO.input(IR_PIN) == GPIO.HIGH:
                return "Object Detected"
            time.sleep(0.1)

    except Exception as e:
        print(f"Error monitoring IR sensor: {e}")
        return None

def send_data_to_server(data):
    try:
        # Connect to the server
        client_socket.connect((server_host, server_port))
        print(f"Connected to server at {server_host}:{server_port}")

        # Send data to the server
        client_socket.sendall(data.encode())
        print(f"Sent '{data}' to the server")

        # Receive data from the server
        response = client_socket.recv(1024).decode()
        print(f"Received '{response}' from the server")

        # IDS functionality
        # Example: Check for SQL injection attempt in response
        if sql_injection_pattern.search(response):
            print("Intrusion Detected: SQL Injection attempt!")

        # Another example: Check for excessive data length
        if len(response) > 1024:
            print("Intrusion Detected: Excessive data length!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    try:
        # Monitor IR sensor for object detection
        object_detected = monitor_ir_sensor()
        if object_detected:
            # Send detection event to server
            send_data_to_server(object_detected)

    except KeyboardInterrupt:
        print("Process interrupted. Cleaning up...")
        GPIO.cleanup()



