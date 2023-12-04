# client

import socket

client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 10000))
print("Connexion établie...")

message = ""
data=""
while message != "bye" and message != "arret" and data != "bye" and data != "arret":
    message = input("vous (bye/arret pour quitter) : ")
    client_socket.send(message.encode())

    if message == "bye" :
        print("Client arrêté.")
        client_socket.close()
    elif message == "arret" :
        print("Server arrêté.")
        client_socket.close()

    if message != "bye" and message != "arret" :
        data = client_socket.recv(1024).decode()
    if data=="bye" or data == "arret":
        client_socket.close()
        break

    print(f"Serveur : {data}")

client_socket.close()
