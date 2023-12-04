import socket
import threading

def receive_messages(sock):
    while True:
        data = sock.recv(1024).decode()
        print(f"Du serveur: {data}")
        if data == "bye" or data == "arret":
            print("Client arrêté.")
            client_socket.close()
            break

def send_messages(sock):
    while True:
        message = input("vous (bye/arret pour quitter) : ")
        sock.send(message.encode())
        if message == "bye" or message == "arret":
            print("Client arrêté.")
            client_socket.close()
            break

if __name__ == '__main__':
    client_socket = socket.socket()
    client_socket.connect(('127.0.0.1', 10000))
    print("Connexion établie...")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    print("Client arrêté.")
    client_socket.close()
