import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QCloseEvent
import socket
import threading

host = "localhost"
port = 10000
DECO = 'deco-server'


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.resize(500, 600)
        self.setWindowTitle('Un logiciel de tchat')
        self.grid = QGridLayout()
        widget.setLayout(self.grid)
        self.setCentralWidget(widget)

        self.serveur = QLabel("Serveur")
        self.entrserv = QLineEdit("localhost")
        self.port = QLabel("Port")
        self.entrport = QLineEdit("10000")
        self.co = QPushButton("Connexion")
        self.affichage = QTextBrowser()
        self.msg = QLabel("Message : ")
        self.message = QLineEdit()
        self.message.setEnabled(False)
        self.envoi = QPushButton("Envoyer")
        self.envoi.setEnabled(False)
        self.effacer = QPushButton("Effacer")
        self.quitter = QPushButton("Quitter")

        self.grid.addWidget(self.serveur, 0, 0)
        self.grid.addWidget(self.entrserv, 0, 1)
        self.grid.addWidget(self.port, 1, 0)
        self.grid.addWidget(self.entrport, 1, 1)
        self.grid.addWidget(self.co, 2, 0, 1, 2)
        self.grid.addWidget(self.affichage, 3, 0, 1, 2)
        self.grid.addWidget(self.msg, 4, 0)
        self.grid.addWidget(self.message, 4, 1)
        self.grid.addWidget(self.envoi, 5, 0, 1, 2)
        self.grid.addWidget(self.effacer, 6, 0, 1, 1)
        self.grid.addWidget(self.quitter, 6, 1, 1, 1)

        self.co.clicked.connect(self._actionCo)
        self.envoi.clicked.connect(self._actionEnv)
        self.effacer.clicked.connect(self._actionEff)
        self.quitter.clicked.connect(self._actionQuit)

    def _actionCo(self):
        self.client = None
        print(f"=============> {self.co.text()}")
        if self.co.text() == "Connexion":
            try:
                print("===============> Ouverture de la connexion ")
                self.client = Client(host, port)
                self.client.connexion()
                self.co.setText("Deconnexion")
                self.envoi.setEnabled(True)
                self.message.setEnabled(True)
            except Exception as e:
                self.affichage.append(f"Erreur de connexion : {e}")
        else:
            try:
                print("===============> Fermeture de la connexion ")
                self.client.kill()
                self.co.setText("Connexion")
                self.envoi.setEnabled(False)
                self.message.setEnabled(False)
            except Exception as e:
                self.affichage.append(f"Erreur de deconnexion : {e}")

    def _actionEnv(self):
        try:
            if self.message.text() == DECO:
                self.client.kill()
                self.closeEvent()

            else:
                self.msgclient = self.message.text()
                self.affichage.append(f"{self.msgclient}")
                self.client.envoi(self.msgclient)

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Une erreur est survenue : ({e})")
            msg.exec()

    def _actionEff(self):
        self.message.clear()

    def _actionQuit(self):
        if self.co.text() == "Deconnexion":
            self.msgclient = DECO
            self.affichage.append(f"{self.msgclient}")
            self.client = Client(host, port)
            self.client.envoi(self.msgclient)


class Client():
    def __init__(self, host, port):
        self.clsocket = None
        self.port = port
        self.host = host
        self.message = ''
        self.iskilled = False

    def connexion(self):
        self.clsocket = socket.socket()
        self.clsocket.connect((self.host, self.port))
        print(self.clsocket)
        thread = threading.Thread(target=self.reception)
        thread.start()

    def envoi(self, message):
        print(self.clsocket)
        if self.clsocket is not None:
            self.clsocket.send(message.encode())
        else:
            print("======= OUlllllaaaaa")

    def reception(self):
        msg = ""
        msgclient = DECO
        while msg != DECO and msgclient != DECO:
            msg = self.clsocket.recv(1024).decode()
            print(msg)

    def kill(self):
        self.iskilled = True
        self.clsocket.send(DECO.encode())
        self.clsocket.close()

    def closeEvent(self, _e: QCloseEvent):  # <--- Fermeture de l'application depuis la croix Windows
        try:
            box = QMessageBox()
            box.setWindowTitle("Quitter ?")
            box.setText("Voulez vous quitter ?")
            box.addButton(QMessageBox.Yes)
            box.addButton(QMessageBox.No)

            ret = box.exec()

            if ret == QMessageBox.Yes:
                Client.kill()
                QCoreApplication.exit(0)
            else:
                _e.ignore()
        except OSError:
            QCoreApplication.exit(0)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec()

    client = Client(host, port)
    try:
        client.connexion()
        # client2 = Client(HOST, int(sys.argv[1]))
        message = ''
        while message != DECO:
            message = input('Entrer une commande: ')
            client.envoi(message)
            # client2.envoi(message)
    except KeyboardInterrupt:
        client.kill()

# https://github.com/julesbrt/R309-prog_evenementielle