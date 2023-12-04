import socket

message = "Bonjour ça va ?"

client_socket = socket.socket()
client_socket.connect(('127.0.0.3', 10000))
print("Connexion établie...")
client_socket.send(message.encode())
print("Message envoyé... en attente d'une réponse")

reply = client_socket.recv(1024).decode()
print(f"serveur : {reply}")


client_socket.close()