import threading
import sys
import time
import socket
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *



host = socket.gethostname() 
port = 10000





class client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chronomètre")
    


        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)
   
   
        self.compteur = QLabel("Compteur : ")

        self.text = QLineEdit("0")
        start = QPushButton("Start")
        reset = QPushButton("Reset")
        stop = QPushButton("Stop")
        quit = QPushButton("Quitter")
        connect = QPushButton("Connect")
        





        grid.addWidget(self.compteur, 0, 0)
        grid.addWidget(self.text, 1, 0,1,0)
        grid.addWidget(quit, 5, 1)
        grid.addWidget(connect, 5, 0)
        grid.addWidget(start, 2, 0,1,0)
        grid.addWidget(reset, 3, 0)
        grid.addWidget(stop, 3, 1)


        
        

        start.clicked.connect(self.__action_start)
        reset.clicked.connect(self.__action_reset)
        stop.clicked.connect(self.__action_stop)
        quit.clicked.connect(self.__quit)
        connect.clicked.connect(self.__connect)

        self.text.setEnabled(False)
    
    def __action_reset(self):
        self.text.setText("0")
        self.compteur.setText("Compteur : ")
    
    def __action_start(self):
        timer = threading.Timer(1, self.__action_start)
        timer.start()
        self.text.setText(str(int(self.text.text()) + 1))
        

    def __action_stop(self):
        timer = threading.Timer(1, self.__action_start)
        timer.stop() 
        self.text.setText(self.text.text())
        

    def __connect(self):
        server_socket = socket.socket()
        server_socket.connect((host, port))
        msg = ""
        while msg != "bye":
            # Réception du message du client
            msg = server_socket.recv(1024).decode()

    def __quit(self):
        self.__action_stop()
        sys.exit()


        






    
if __name__ == "__main__":

    print(f"Ouverture de la socket sur le serveur {host} port {port}")
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print("Serveur est connecté")

    app = QApplication(sys.argv)
    window = client()
    window.show()
    app.exec()


#