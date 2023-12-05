import socket
import threading
import time

clients = []
client_threads = []  # Nouvelle liste pour stocker les threads des clients
server_socket = socket.socket()
server_running = True  # Ajout de la variable pour contrôler l'état du serveur

def ecoute(conn, addr):
    global clients, server_running
    while True:
        try:
            message = conn.recv(1024).decode()
            if message == "arret":
                print(f"Client {addr} a été notifié de l'arrêt du serveur.")
                for client, _ in clients:
                    client.send("arret".encode())
                break
            elif message == "bye":
                print(f"Client {addr} a quitté la conversation.")
                conn.send("Fin".encode())
                break
            else:
                for client, client_addr in clients:
                    if (client, client_addr) != (conn, addr):
                        client.send(f"Client {addr}: {message}".encode())
        except ConnectionResetError:
            print(f"Client {addr} déconnecté de manière inattendue.")
            break
    conn.close()
    clients.remove((conn, addr))

def accepter_connexions():
    global clients, client_threads, server_running
    while server_running:
        try:
            print("En attente de clients...")
            conn, address = server_socket.accept()
            print(f"Nouveau client connecté : {address}")
            clients.append((conn, address))
            t = threading.Thread(target=ecoute, args=(conn, address))
            t.start()
            client_threads.append(t)  # Ajoutez le thread à la liste
        except socket.error as e:
            print(f"Erreur lors de l'acceptation de la connexion : {e}")

def arreter_clients():
    global clients, client_threads
    for client, _ in clients:
        try:
            client.send("arret".encode())
            client.close()
        except socket.error as e:
            print(f"Erreur lors de l'arrêt du client : {e}")

    # Attendre que tous les threads clients soient terminés
    for thread in client_threads:
        thread.join()

def main():
    global server_running
    t_accept = threading.Thread(target=accepter_connexions)
    t_accept.start()

    input("Appuyez sur Entrée pour arrêter le serveur...\n")

    # Modifier l'état du serveur pour déclencher l'arrêt
    server_running = False

    # Arrêter tous les clients
    arreter_clients()

    server_socket.close()

if __name__ == "__main__":
    try:
        server_socket.bind(('127.0.0.1', 5546))
        server_socket.listen()
        main()
    except socket.error as e:
        print(f"Erreur lors de la création du socket : {e}")
