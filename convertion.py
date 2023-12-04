import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QGridLayout, QLabel, QLineEdit, QComboBox

class TemperatureConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertisseur de Température")
        self.resize(300, 150)
        self.setup_ui()

    def setup_ui(self):
        # Création des widgets
        self.label = QLabel("Température : ")
        self.label2 = QLabel("°C")
        self.line_edit = QLineEdit()
        self.button = QPushButton("Convertir")
        self.text = QLabel("")
        self.quit_button = QPushButton("Quitter")
        self.help_button = QPushButton("?")

        # Menu déroulant pour choisir la conversion
        self.menu = QComboBox()
        self.menu.addItem("°C -> K")
        self.menu.addItem("K -> °C")
        self.menu.currentIndexChanged.connect(self.handle_conversion_change)

        # Connexion des signaux aux slots
        self.button.clicked.connect(self.convert_temperature)
        self.quit_button.clicked.connect(self.close_application)
        self.help_button.clicked.connect(self.show_help)

        # Mise en place du layout
        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.line_edit, 0, 1)
        layout.addWidget(self.label2, 0, 2)
        layout.addWidget(self.menu, 0, 3)
        layout.addWidget(self.button, 1, 0, 1, 2)
        layout.addWidget(self.text, 2, 0, 1, 2)
        layout.addWidget(self.help_button, 1, 3)
        layout.addWidget(self.quit_button, 3, 0, 1, 2)

        self.setLayout(layout)

    def show_help(self):
        QMessageBox.information(self, "Aide", "Permet de convertir un nombre soit de kelvin vers celsius, ou soit de Celcius vers Kelvin.")

    def handle_conversion_change(self):
        # Gestion du changement d'unités
        if self.line_edit.text():
            try:
                temperature = float(self.line_edit.text())
                if temperature == -273.15:
                    self.text.setText("Température du zéro absolu = 0")
                if temperature < -273.15:
                    QMessageBox.critical(self, "Erreur", "La température ne peut pas être inférieure à -273.15°C.")
                    self.line_edit.clear()

            except ValueError:
                QMessageBox.critical(self, "Erreur", "Entrez une température valide.")

    def convert_temperature(self):
        try:
            temperature = float(self.line_edit.text())
            if self.menu.currentIndex() == 0:
                kelvin = temperature + 273.15
                self.text.setText(f"{kelvin:.2f} K")
                self.label2.setText("K")


            else:
                celsius = temperature - 273.15
                self.text.setText(f"{celsius:.2f} °C")
                self.label2.setText("°C")
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Entrez une température valide.")

    def close_application(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = TemperatureConverter()
    converter.show()
    sys.exit(app.exec())
