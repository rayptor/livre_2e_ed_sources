class Distributeur:
    capacite:int = 50
    def __init__(self, reserve: int, prix: float) -> None:
        self.reserve: int = reserve
        self.prix: float = prix

    def acheter(self, quantite: int) -> None:
        if quantite <= 1:
            raise ValueError("Acheter 1 bouteille minimum.")
        if quantite > self.reserve:
            raise ValueError("Plus assez de stock.")
        self.reserve -= quantite
        aPayer = quantite * self.prix
        print(f"{quantite} bouteilles à {self.prix} € : \
total à payer {aPayer} €.")

    def reste(self) -> int:
        return f"Il en reste {self.reserve} sur \
{self.capacite} en stock."

    def __getitem__(self, cle: str) -> int:
        if cle == "reserve":
            return self.reserve
        elif cle == "prix":
            return self.prix
        else:
            raise KeyError(f"{cle} est une clé inconnue.")

		# Avec | la 'valeur' peut être un 'int' ou un 'float'
    def __setitem__(self,
		cle: str,
		valeur: int | float) -> None:
        if cle == "reserve":
            if self.reserve + valeur > self.capacite:
                print(f"Le livreur repart avec \
{self.reserve + valeur - self.capacite} bouteille(s) \
en trop.")
                self.reserve = self.capacite
            else:
                self.reserve += valeur
            print(f"Le stock actuel est de : {self.reserve}.")
        elif cle == "prix":
            self.prix = valeur
            print(f"Le nouveau prix est de : {self.prix} €.")
        else:
            raise KeyError(f"On ne peut changer que \
la quantité du stock et le prix.")

d = Distributeur(50, 1.8)
d.acheter(15)
d.reste()
d["reserve"] = 20
d["prix"] = 2.3
d.acheter(10)
d.reste()
