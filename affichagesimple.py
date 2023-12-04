import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout


class MonApplication(QWidget):
    def __init__(self):
        super().__init__()

        # Création des widgets
        self.label_nom = QLabel("Entrez votre nom:")
        self.nom_edit = QLineEdit()
        self.bouton_ok = QPushButton("OK")
        self.label_message = QLabel()  # Message affiché au-dessus du bouton Quitter
        self.bouton_quitter = QPushButton("Quitter")

        # Connexion du signal "clicked" du bouton OK à la fonction correspondante
        self.bouton_ok.clicked.connect(self.afficher_message)

        # Connexion du signal "clicked" du bouton Quitter à la fonction correspondante
        self.bouton_quitter.clicked.connect(self.quitter_application)

        # Mise en page verticale
        layout = QVBoxLayout()
        layout.addWidget(self.label_nom)
        layout.addWidget(self.nom_edit)
        layout.addWidget(self.bouton_ok)
        layout.addWidget(self.label_message)  # Message au-dessus du bouton Quitter
        layout.addWidget(self.bouton_quitter)

        # Définition du layout principal de la fenêtre
        self.setLayout(layout)

        # Titre de la fenêtre
        self.setWindowTitle("Exercice 1 : Interface graphique")

    def afficher_message(self):
        # Récupérer le texte saisi dans la zone de texte
        nom = self.nom_edit.text()

        # Afficher le message sur l'interface graphique
        self.label_message.setText(f"Bonjour {nom}")

    def quitter_application(self):
        # Fermer l'application lorsque le bouton Quitter est cliqué
        app.quit()


if __name__ == '__main__':
    # Créer l'application PyQt
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre
    fenetre = MonApplication()
    fenetre.show()

    # Exécuter l'application
    sys.exit(app.exec())
