try:
    nom_fichier = "fichier.txt"

    with open(nom_fichier, 'r') as fichier:
        for ligne in fichier:
            ligne = ligne.rstrip("\n\r")
            print(ligne)
except FileNotFoundError as e:
    print("Erreur : Le fichier spécifié n'a pas été trouvé.")
except IOError as e:
    print("Erreur d'entrée/sortie : Une erreur s'est produite lors de la lecture du fichier.")
except PermissionError as e:
    print("Erreur de permission : Vous n'avez pas la permission d'accéder au fichier.")
except Exception as e:
    print(f"Une erreur inattendue s'est produite : {str(e)}")
finally:
    print("Fin du programme.")