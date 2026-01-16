import socket
import sys
import threading

if len(sys.argv) != 2:
    print("Usage: python client.py <Name>")
    exit()

name = sys.argv[1]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8080))

client_socket.send(name.encode())

def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            print(msg)
        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    message = input()

    if message == "EXIT":
        client_socket.send("EXIT".encode())
        break

    client_socket.send(message.encode())

client_socket.close()