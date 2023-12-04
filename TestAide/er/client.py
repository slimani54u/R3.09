#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QTextBrowser,
)
from PyQt5.QtCore import Qt, QCoreApplication
import logging
import threading
import socket

logging.basicConfig(level=logging.DEBUG)

# Alors ça segfault aléatoirement lors de l'échange de message
# et a chaque fois lors de la déconnexion, sûrement un rapport
# avec la façon dont le thread est fermé. Je crois que le socket
# est fermé avant que le thread soit stoppé???
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.__connected = False

        self.__client = socket.socket()

        # Labels
        self.__LabelServeur = QLabel("Serveur")
        self.__LabelPort = QLabel("Port")
        self.__LabelMessage = QLabel("Message:")

        # LineEdits
        self.__LineEditServeur = QLineEdit("localhost")
        self.__LineEditPort = QLineEdit("10000")
        self.__LineEditMessage = QLineEdit()

        # Buttons
        self.__ButtonConnexion = QPushButton("Connexion")
        self.__ButtonMessage = QPushButton("Envoyer")
        self.__ButtonEffacer = QPushButton("Effacer")
        self.__ButtonQuitter = QPushButton("Quitter")

        # QTextBrowser
        self.__TextBrowser = QTextBrowser()

        self.__ButtonMessage.setEnabled(False)
        self.__LineEditMessage.setEnabled(False)

        ### --- PLACEMENTS --- ### row: int, column: int, rowSpan: int, columnSpan: int
        # Partie connexion
        grid.addWidget(self.__LabelServeur, 0, 0)
        grid.addWidget(self.__LineEditServeur, 0, 1)

        grid.addWidget(self.__LabelPort, 1, 0)
        grid.addWidget(self.__LineEditPort, 1, 1)

        grid.addWidget(self.__ButtonConnexion, 2, 0, 1, 2)

        # Partie message
        grid.addWidget(self.__TextBrowser, 3, 0, 1, 2)

        grid.addWidget(self.__LabelMessage, 4, 0)
        grid.addWidget(self.__LineEditMessage, 4, 1)
        grid.addWidget(self.__ButtonMessage, 5, 0, 1, 2)


        # Partie quitter
        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        l.addWidget(self.__ButtonEffacer)
        l.addWidget(self.__ButtonQuitter)
        grid.addWidget(w, 6, 0, 1, 2)

        self.__ButtonConnexion.clicked.connect(self.__connexion)
        self.__ButtonMessage.clicked.connect(self.__envoi)
        self.__LineEditMessage.returnPressed.connect(self.__envoi)
        self.__ButtonEffacer.clicked.connect(lambda: self.__TextBrowser.clear())
        self.__ButtonQuitter.clicked.connect(self.__quitter)


    def __connexion(self):
        if not self.__connected:
            host = self.__LineEditServeur.text()
            port = self.__LineEditPort.text()
            try:
                port = int(port)
            except ValueError as e:
                self.ErrorBox(e, "Le port est invalide")
            else:
                try:
                    self.__client.connect((host, port))
                except Exception as e:
                    self.ErrorBox(e, f"Erreur de connexion avec le serveur {host}:{port}!")
                else:
                    self.__ButtonConnexion.setText("Déconnexion")
                    self.__connected = True
                    self.__TextBrowser.append(f"Connecté à {host}:{port}")
                    self.__ButtonMessage.setEnabled(True)
                    self.__LineEditMessage.setEnabled(True)
                    client_handler = threading.Thread(target=self.__recv)
                    client_handler.start()
        else:
            try:
                self.__client.send("deco-server".encode())
            except Exception as e:
                self.ErrorBox(e, "Erreur lors de la déconnexion!")
            else:
                self.__connected = False
                print("close socket")
                self.__client.close()
                self.__ButtonConnexion.setText("Connexion")
            finally:
                self.__ButtonMessage.setEnabled(False)
                self.__LineEditMessage.setEnabled(False)

    def __envoi(self):
        msgcl = self.__LineEditMessage.text()
        try:
            self.__client.send(msgcl.encode())
        except Exception as e:
            self.ErrorBox(e, "Erreur lors de l'envoi du message!")
        else:
            print(f"Envoi: {msgcl}")
            self.__LineEditMessage.setText("")
            self.__TextBrowser.append(msgcl)
            self.__TextBrowser.setAlignment(Qt.AlignLeft)
    
    # Comme le serveur n'est pas asynchrone le bouton ne marche pas quand c'est au tour du serveur de parler
    def __quitter(self):
        if self.__connected:
            try:
                print("deconnexion")
                self.__client.send("deco-server".encode())
            except Exception as e:
                print(f"erreur lors de la fermeture {e}")
            else:
                self.__connected = False
            finally:
                QCoreApplication.exit(0)

    def __recv(self):
            msgsrv = ""
            print("recv start")
            while msgsrv != "deco-server" and self.__connected:
                try:
                    msgsrv = self.__client.recv(1024).decode()
                except Exception as e:
                    self.ErrorBox(e, "Erreur pendant la réception!")
                self.__TextBrowser.append(msgsrv)
                self.__TextBrowser.setAlignment(Qt.AlignRight)
            print("recv stop")

    def InfoBox(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec()

    def ErrorBox(self, e, message: str = ""):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"{message} ({e})")
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
