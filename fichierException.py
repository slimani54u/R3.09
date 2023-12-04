if __name__ == '__main__':
    fichier='f.txt'
    try:
        with open(fichier, 'r') as f:
            for l in f:
                l = l.rstrip("\n\r")
                #parceque si j'enleve \n le fichier n'elever pas les retours a la lignes
                print(l)
        f.close()
    except FileNotFoundError:
        print(" le fichier n'a pas était trouvé")
    except IOError:
        print("erreur de lecture ecritutre")
    except FileExistsError:
        print("Fichier existe déjà")
    except PermissionError:
        print("je n'ai pas les droits")
    finally:
        print("ce programe est fini")

