import socket
message ="bien et toi ? "
server_socket = socket.socket()
print("Socket crée, en attente du client...")

server_socket.bind(('0.0.0.0',10000))
server_socket.listen(1)

conn, address = server_socket.accept()
print("Connexion établie...")

reply= conn.recv(1024).decode()
conn.send(reply.encode())
print(f"de {address} : {reply}")

conn.close()
server_socket.close()