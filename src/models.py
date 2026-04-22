# src/models.py
"""
Bloc 3 - Architecture POO
Classes : Salle et Reservation
"""


class Salle:
    """Représente une salle de l'université."""

    def __init__(self, nom: str, capacite: int, equipements: list, disponible: bool = True):
        self.nom = nom
        self.capacite = capacite
        self.equipements = equipements
        self.disponible = disponible

    def est_disponible(self) -> bool:
        """Retourne True si la salle est disponible."""
        return self.disponible

    def __str__(self) -> str:
        statut = "Disponible" if self.disponible else "Indisponible"
        return f"Salle {self.nom} | Capacité : {self.capacite} | {statut} | Équipements : {self.equipements}"


class Reservation:
    """Représente une réservation de salle."""

    def __init__(self, id: int, salle: Salle, jour: str, creneau: str, utilisateur: str):
        self.id = id
        self.salle = salle
        self.jour = jour
        self.creneau = creneau
        self.utilisateur = utilisateur

    def __str__(self) -> str:
        return (f"Réservation #{self.id} | Salle : {self.salle.nom} | "
                f"{self.jour} {self.creneau} | Par : {self.utilisateur}")