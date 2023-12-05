import socket

client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 10000))
print("Connexion établie...")
data=""
while True:
    message = input("vous (bye/arret pour quitter) : ")
    client_socket.send(message.encode())

    if message == "arret" or message=="bye":
        print("Client arrêté.")
        client_socket.close()
        break

    data = client_socket.recv(1024).decode()
    if data == "arret" or data=="bye":
        print("Client et serveur arrêté.")
        client_socket.close()
        break
    print(f"Serveur : {data}")

client_socket.close()
