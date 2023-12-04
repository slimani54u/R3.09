import socket
import threading

def receive_messages(sock, addr):
    while True:
        data = sock.recv(1024).decode()
        print(f"De {addr}: {data}")
        if data == "bye":
            print("Fermeture de la socket cliente")
            conn.close()
        elif data == "arret":
            print("Fermeture de la socket cliente")
            server_socket.close()
            break

def send_messages(sock):
    while True:
        message = input("vous (bye/arret pour quitter) : ")
        sock.send(message.encode())
        if message == "bye" or message == "arret":
            print("Fermeture de la socket cliente")
            conn.close()
            break
    server_socket.close()
if __name__ == '__main__':
    server_socket = socket.socket()
    print("Socket créé, en attente du client...")
    server_socket.bind(('0.0.0.0', 10000))
    server_socket.listen()

    conn, address = server_socket.accept()
    print("Connexion établie avec", address)

    receive_thread = threading.Thread(target=receive_messages, args=(conn, address))
    send_thread = threading.Thread(target=send_messages, args=(conn,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    print("Fermeture de la socket cliente")
    conn.close()
    server_socket.close()
