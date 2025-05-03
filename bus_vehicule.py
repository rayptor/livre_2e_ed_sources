from abc import ABC, abstractmethod

class Vehicule(ABC):
    @abstractmethod
    def afficher_places(self) -> None:
        pass
    
    @abstractmethod
    def afficher_energie(self) -> None:
        pass

    @abstractmethod
    def afficher_couleur(self) -> None:
        pass

    @abstractmethod
    def afficher_options(self) -> None:
        pass

    def afficher_autre(self):
        raise NotImplemented

    @classmethod
    def afficher_type(cls) -> None:
        print(f"Ce véhicule est bien de type '{cls.__name__}' "
              f"et hérite de {cls.__bases__}.")


class Voiture(Vehicule):
    __slots__ = ("places", "energie", "couleur")
    def __init__(self,
                 places: int,
                 energie: str,
                 couleur: str
            ) -> None:
        self.places = places
        self.energie = energie
        self.couleur = couleur

    def afficher_places(self) -> None:
        print(f"Ce véhicule a {self.places} places.")

    def afficher_energie(self) -> None:
        print(f"Ce véhicule utilise l'énergie {self.energie}.")

    def afficher_couleur(self) -> None:
        print(f"La couleur est {self.couleur}.")

    def afficher_options(self) -> None:
        print(f"Aucune option spécifique définie pour ce véhicule de type "
              f"{self.__class__}.")

    def __str__(self) -> str:
        return (f"Ce véhicule {self.energie} de couleur {self.couleur} "
                f"a {self.places} places.")

    def __repr__(self) -> str:
        return (f"{self.__class__.__qualname__}, "
                f"{self.energie}, {self.places}, {self.couleur}")

class Bus(Voiture):
    monType = "bus"

    def __init__(self,
            places: int,
            energie: str,
            couleur: str,
            prioritaire: bool
        ) -> None:
        super().__init__(places, energie, couleur)
        self.prioritaire = prioritaire

    def afficher_type(self) -> None:
        print(f"Ce véhicule est bien un {self.monType}.")

    def afficher_options(self) -> None:
        print(f"Aucune option spécifique définie pour ce véhicule de type {self.__class__}.")

    def __str__(self) -> str:
        priority = "est prioritaire" if self.prioritaire else "n'est pas prioritaire"
        return (f"Ce bus {self.couleur} {self.energie} de {self.places} places "
                f"{priority}.")

    def __repr__(self) -> str:
        return (f"{self.__class__.__qualname__}, {self.prioritaire}, "
                f"{self.energie}, {self.places}, {self.couleur}")

if __name__ == "__main__":
    v = Voiture(5, "thermique", "bleue")
    print(v)
    v.afficher_places()
    v.afficher_energie()
    v.afficher_couleur()
    print("-" * 30)
    b = Bus(40, "thermique", "rouge", True)
    print(b)
    b.afficher_couleur()
    b.afficher_type()
    print("-" * 30)
    v1 = Voiture(2, "thermique", "rouge")
    b1 = Bus(24, "thermique", "noir", True)
    print(f"v1 is Voiture: {type(v1) == Voiture}")
    print(f"b1 is Vehicule: {type(b1) == Vehicule}")
    print(f"b1 is Bus: {type(b1) == Bus}")
    print(f"v1 isinstance Voiture: {isinstance(v1, Voiture)}")
    print(f"b1 isinstance Voiture: {isinstance(b1, Voiture)}")
    print(f"b1 isinstance Bus: {isinstance(b1, Bus)}")
    print("-" * 30)
    print(f"Bus subclass of Voiture: {issubclass(Bus, Voiture)}")
    print(f"bool subclass of int: {issubclass(bool, int)}")
    print("-" * 30)
    v1 = Voiture(2, "thermique", "rouge")
    print(v1)
    v1.afficher_type()
    v2 = Voiture(5, "hybride", "bleue")
    print(v2)
    v2.afficher_type()
    v3 = Bus(40, "thermique", "gris", True)
    print(v3)
    v3.afficher_type()
    v4 = Bus(10, "électrique", "vert", False)
    print(v4)
    v4.afficher_type()
    print("-" * 30)
    v.afficher_options()
    b.afficher_options()
