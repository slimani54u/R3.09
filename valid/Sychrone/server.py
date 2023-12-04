import socket

server_socket = socket.socket()
print("Socket créé, en attente du client...")
server_socket.bind(('127.0.0.1', 10000))
server_socket.listen(1)
reply=""
while True:
    conn, address = server_socket.accept()
    print("Connexion établie avec", address)
    reply = ""
    while True:
        data = conn.recv(1024).decode()



        print(f"De {address} : {data}")

        if data == "bye" or reply=="bye":
            print("Client déconnecté.")
            break
        elif data == "arret" or reply == "arret":
            print("Client et serveur déconnectés.")
            conn.close()
            server_socket.close()
            break
        else:
            reply = input("vous : ")

        conn.send(reply.encode())



server_socket.close()
