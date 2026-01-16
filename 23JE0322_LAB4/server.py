import socket
import os

HOST = "localhost"
PORT = 8080
BUFFER_SIZE = 1024
EOF_MARKER = b"__EOF__"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print("Server is listening on port 8080...")

    client_socket, client_address = server_socket.accept()
    print(f"Connected to client at {client_address}")

    try:
        #  1: receiving file name
        filename = client_socket.recv(BUFFER_SIZE).decode()
        if not filename:
            print("No filename received.")
            return

        print(f"Receiving file: {filename}")

        # ensuring file is saved safely
        filename = os.path.basename(filename)

        with open(filename, "wb") as file:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if data == EOF_MARKER:
                    break
                file.write(data)

        print(f"File {filename} received successfully.")

        #  4: sending ACK
        client_socket.send(b"ACK")

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    main()