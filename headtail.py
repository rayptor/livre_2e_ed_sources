import sys

def head(nom: str, n: int) -> None:
    with open(nom, "r") as fichier:
        ligne = fichier.readline()
        compteur: int = 0
        print(f"Les {n} premières lignes sont :")
        for i in range(n):
            print("> ", ligne, end = "")
            ligne = fichier.readline()
            i += 1


def tail(nom: str, n: int) -> None:
    with open(nom, "r") as fichier:
        lignes = []
        for ligne in fichier:
            lignes.append(ligne)
            if len(lignes) > n:
                lignes.pop(0)

    print(f"Les {n} dernières lignes sont :")
    for l in lignes:
        print("> ", l, end = "")

if __name__ == "__main__":
    args = sys.argv[:]
    nombre: int = 0
    fichier: str = ""
    
    nombre = int(args[2])
    fichier = args[4]
    head(fichier, nombre)
    print("")
    tail(fichier, nombre)

    

