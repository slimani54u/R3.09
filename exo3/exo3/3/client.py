# client

import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data == "bye" or data == "arret":
                print(f"Serveur : {data}")
                client_socket.close()
                break
            print(f"Serveur : {data}")
        except ConnectionResetError:
            break

def start_client():
    client_socket = socket.socket()
    client_socket.connect(('127.0.0.1', 10000))
    print("Connexion établie...")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("vous (bye/arret pour quitter) : ")
        client_socket.send(message.encode())

        if message == "bye" or message == "arret":
            print(f"Client arrêté.")
            client_socket.close()
            break

if __name__ == '__main__':
    start_client()
    receive_messages()
