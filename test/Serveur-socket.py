#server

import socket
import threading

exit_thread = False
def conn_rep(conn):
    data = conn.recv(1024).decode()

    while data != "bye" and data != "arret" :

        data = conn.recv(1024).decode()
        print(f"De {address} : {data}")




    print("Fermeture de la socket cliente")



if __name__ == '__main__':



    server_socket = socket.socket()
    print("Socket créé, en attente du client...")
    server_socket.bind(('0.0.0.0', 10000))
    server_socket.listen()
    conn, address = server_socket.accept()
    data = ""
    reply = ""
    while reply != "arret" and reply != "bye":


        client_thread = threading.Thread(target=conn_rep, args=[conn])
        client_thread.start()

        print("Connexion établie avec", address)
        while data != "bye" and data != "arret":

            reply = input("vous : ")
            conn.send(reply.encode())
            print(f"{reply} envoyé")





    conn.close()
    server_socket.close()
    client_thread.join()
