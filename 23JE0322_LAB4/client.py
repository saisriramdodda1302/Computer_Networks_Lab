import socket
import sys
import os

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024
EOF_MARKER = b"__EOF__"

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <filename>")
        return

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print("Error: File not found.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print("Connected to the server.")
        print(f"Sending file: {filename}")

        # 1: sending file name
        client_socket.send(filename.encode())

        # 2: sending file data in chunks
        with open(filename, "rb") as file:
            while True:
                chunk = file.read(BUFFER_SIZE)
                if not chunk:
                    break
                client_socket.send(chunk)

        # 3: sending EOF marker
        client_socket.send(EOF_MARKER)

        # 4: Receive ACK
        ack = client_socket.recv(BUFFER_SIZE).decode()
        if ack == "ACK":
            print(f"File {filename} sent successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
