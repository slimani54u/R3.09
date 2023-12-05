import threading
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QTextEdit
import socket

class ChatBot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Le serveur de tchat")
        self.resize(300, 400)
        self.label = QLabel("Serveur")
        self.line_edit = QLineEdit("127.0.0.1")
        self.label2 = QLabel("Port")
        self.line_edit2 = QLineEdit("10000")
        self.button = QPushButton("le serveur Démarre")
        self.label3 = QLabel("Nombre maximum de clients")
        self.line_edit3 = QLineEdit("5")
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.label.setText("Serveur")
        self.label2.setText("Port")
        self.label3.setText("Nombre maximum de clients")
        self.button.clicked.connect(self.__demarrage)

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.line_edit, 0, 1)
        layout.addWidget(self.label2, 1, 0)
        layout.addWidget(self.line_edit2, 1, 1)
        layout.addWidget(self.label3, 2, 0)
        layout.addWidget(self.line_edit3, 2, 1)
        layout.addWidget(self.button, 3, 0, 1, 3)
        layout.addWidget(self.text_edit, 4, 0, 1, 3)
        self.setLayout(layout)

    def __demarrage(self):
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur.bind((self.line_edit.text(), int(self.line_edit2.text())))
        self.serveur.listen(int(self.line_edit3.text()))
        self.button.setText("Arrêt du serveur")
        self.label.setText("Serveur démarré")
        self.button.clicked.connect(self.__arret)
        self.label2.setText("Attente de connexion")
        self.label3.setText("Nombre de clients connectés : 0")
        self.thread_accept = threading.Thread(target=self.__accept)
        self.thread_accept.start()

    def __arret(self):
        self.serveur.close()

        self.button.clicked.connect(self.__demarrage)
        self.button.setEnabled(True)
        self.text_edit.clear()

    def __accept(self):
        while True:
            try:
                self.connexion, self.adresse = self.serveur.accept()
                self.label2.setText("Connexion établie avec {}".format(self.adresse))
                self.thread___reception = threading.Thread(target=self.__reception)
                self.thread___reception.start()
            except Exception :
                print(f"erreur dans la connexion avec le client")

    def __reception(self):
        try:
            while True:
                self.message_recu = self.connexion.recv(1024).decode()
                if not self.message_recu:
                    break
                self.text_edit.append(self.message_recu)
                self.label3.setText("Nombre de clients connectés : {}".format(len(threading.enumerate()) - 2))
        except Exception:
            print("Client déconnecté")
        finally:
            self.connexion.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ChatBot = ChatBot()
    ChatBot.show()
    sys.exit(app.exec())


#lien github
#https://github.com/slimani54u/R3.09