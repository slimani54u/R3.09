# server

import socket
import threading

def handle_client(conn, address):
    data = ""
    reply = ""

    while data != "arret" and reply != "arret":
        data = conn.recv(1024).decode()
        print(f"De {address} : {data}")

        if data != "bye" and data != "arret":
            reply = input("vous : ")
            conn.send(reply.encode())
            print(f"{reply} envoyé")

    print("Fermeture de la socket cliente")
    conn.close()
    if data == "arret" or reply == "arret":
        print("Arrêt du serveur")
        server_socket.close()


if __name__ == '__main__':
    server_socket = socket.socket()
    print("Socket créé, en attente du client...")
    server_socket.bind(('0.0.0.0', 10000))
    server_socket.listen()

    while True:
        print("En attente du client")
        conn, address = server_socket.accept()
        print("Connexion établie avec", address)

        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()

    server_socket.close()
