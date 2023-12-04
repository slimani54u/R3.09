import sys
import socket
import threading
import time
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QPushButton, QLabel, QGridLayout, QWidget, QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.__compt = QLabel("Compteur : ")
        self.text = QLabel("0")
        self.y = 0
        self.client_socket = None
        self.arret_thread = False
        self.thread = None
        reset = QPushButton("Reset")
        quit = QPushButton("Quitter")
        start = QPushButton("Start")
        connect = QPushButton("Connect")
        stop = QPushButton("Stop")


        grid.addWidget(self.__compt, 0, 0, 1, 2)#taille(1 ligne,2 colonne)
        grid.addWidget(self.text, 1, 0, 1, 2)
        grid.addWidget(stop, 3, 1)
        grid.addWidget(connect, 4, 0)
        grid.addWidget(reset, 3, 0)
        grid.addWidget(start, 2, 0, 1, 2)
        grid.addWidget(quit, 4, 1)

        reset.clicked.connect(self.__reset)
        quit.clicked.connect(self.__actionQuitter)
        start.clicked.connect(self.__start)
        connect.clicked.connect(self.__connect)
        stop.clicked.connect(self.__stop)
        self.setWindowTitle("Chronomètre")

    def __start(self):
        self.arret_thread = False

        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.__thread_function)
            self.thread.start()

    def __thread_function(self):
        while not self.arret_thread:
            time.sleep(1)
            self.y += 1
            self.text.setText(str(self.y))

            if self.client_socket:
                try:
                    self.client_socket.sendall(str(self.y).encode())
                except Exception :
                    print(f"Erreur d'envoi de message au serveur")

    def __stop(self):
        self.arret_thread = True
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def __reset(self):
        self.y = 0
        self.text.setText(str(self.y))

    def __actionQuitter(self):
        self.__stop()
        msg = "bye"
        if self.client_socket:
            try:
                self.client_socket.sendall(str(msg).encode())
            except Exception as e:
                print(f"Erreur lors de l'envoi du message au serveur : {e}")

        QCoreApplication.exit(0)

    def __connect(self):
        self.client_socket = socket.socket()
        try:
            self.client_socket.connect(("localhost", 10000))
            print("Le client vient de se connecter")
        except Exception as e:
            print(f"Erreur de connexion au serveur")
            self.client_socket.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
