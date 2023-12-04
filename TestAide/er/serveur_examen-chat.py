#!/usr/bin/env python3
import socket

host = "localhost" # "", "127.0.0.1
port = 10000

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)

print('En attente du client')
conn, address = server_socket.accept()
print(f'Client connecté {address}')

msg = ""
while msg != "deco-server":
    # Réception du message du client
    msg = conn.recv(1024).decode()
    print(f"Message reçu du client : {msg}")
    if msg != "deco-server":
        msg = input("Message : ")
    
    conn.send(msg.encode())
    print(f"Message envoyé : {msg}")

# Fermeture
conn.close()
print("Fermeture de la socket client")
server_socket.close()
print("Fermeture de la socket serveur")
