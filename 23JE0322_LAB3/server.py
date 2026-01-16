import socket
import threading
from datetime import datetime

clients = {} # socket -> name
msg_count = {} # name -> number of messages
lock = threading.Lock()

log_file = open("server_logs.txt", "a")

def broadcast(sender_socket, message):
    for sock in clients:
        if sock != sender_socket:
            try:
                sock.send(message.encode())
            except:
                pass

def handle_client(client_socket, client_address):
    try:
        name = client_socket.recv(1024).decode()
    except:
        client_socket.close()
        return

    with lock:
        clients[client_socket] = name
        msg_count[name] = 0

    print(f"{name} joined from {client_address}")
    broadcast(client_socket, f"{name} joined the chat")

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode()

            if message == "EXIT":
                break

            if message == "LIST":
                with lock:
                    names = ", ".join(clients.values())
                client_socket.send(f"Connected users: {names}".encode())
                continue

            time = datetime.now().strftime("%H:%M:%S")

            #private Message
            if message.startswith("@"):
                try:
                    target, msg = message.split(" ", 1)
                    target = target[1:]
                    found = False

                    with lock:
                        for sock, n in clients.items():
                            if n == target:
                                sock.send(f"[{time}] [PM] {name}: {msg}".encode())
                                found = True

                    if not found:
                        client_socket.send("User not found".encode())
                    continue
                except:
                    client_socket.send("Invalid private message format".encode())
                    continue

            formatted = f"[{time}] {name}: {message}"

            with lock:
                msg_count[name] += 1
                log_file.write(formatted + "\n")
                log_file.flush()

            broadcast(client_socket, formatted)

        except:
            break

    with lock:
        print(f"{name} disconnected. Messages sent: {msg_count[name]}")
        del clients[client_socket]

    broadcast(client_socket, f"{name} left the chat")
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8080))
    server_socket.listen(10)

    print("Chat Server running on port 8080...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()