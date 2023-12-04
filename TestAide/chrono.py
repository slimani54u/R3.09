#https://github.com/2bFaycal/Exam

import threading
import socket
import time
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

class chrono(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chronomètre")

        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)

        self.lab1 = QLabel("compteur:")
        self.lab2 = QLabel("0")

        start = QPushButton("Start")
        reset = QPushButton("Reset")
        stop = QPushButton("Stop")
        connect = QPushButton("Connect")
        quit = QPushButton("Quit")
        quit.clicked.connect(self.close)

        grid.addWidget(self.lab1, 0, 0)
        grid.addWidget(self.lab2, 1, 0)
        grid.addWidget(start, 2, 0, 1, 2)
        grid.addWidget(reset, 3, 0)
        grid.addWidget(stop, 3, 1)
        grid.addWidget(connect, 4, 0)
        grid.addWidget(quit, 4, 1)

        start.clicked.connect(self.__actionstart)
        reset.clicked.connect(self.__actionreset)
        stop.clicked.connect(self.__actionstop)
        connect.clicked.connect(self.__actionconnect)
        quit.clicked.connect(self.__actionquit)


    def __actionstart(self):
        timer = threading.Timer(1, self.__actionstart)
        timer.start()
        self.lab2.setText(str(int(self.lab2.text()) + 1))

    def __actionreset(self):
        reset = 0
        self.lab2.setText(str(reset))


    def __actionstop(self):
        timer = threading.Timer(1, self.__actionstart)
        timer.cancel()
        self.lab2.setText(str(int(self.lab2.text())))

 
 
    def __actionconnect(self):
        msg = ""
        


    def __actionquit(self):
        msg = "bye"
        chrono.send(msg.encode())
        print ('requête arret envoyé')
        data = chrono.recv(1024).decode()
        print ('réponse du serveur :', data)








if __name__ == "__main__":

    host = "localhost"
    port = 10000

    print("client se connecte au serveur")
    client_socket = socket.socket()

    client_socket.connect((host, port))
    print("Client connecté au serveur")


    app = QApplication(sys.argv)

    window = chrono()
    window.show()
    app.exec()


    #python3 C:\Users\fayca\OneDrive\Bureau\BloulFayal309\chrono.py