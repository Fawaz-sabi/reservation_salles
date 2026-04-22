# src/planning.py
"""
Bloc 3 - Architecture POO
Classe : Planning
"""

from models import Salle, Reservation


class Planning:
    """Gère l'ensemble des réservations de salles."""

    def __init__(self):
        self.reservations = []

    def detecter_conflit(self, salle: Salle, jour: str, creneau: str) -> bool:
        """Retourne True si un conflit existe pour ce créneau."""
        return any(
            r.salle.nom == salle.nom and r.jour == jour and r.creneau == creneau
            for r in self.reservations
        )

    def ajouter_reservation(self, salle: Salle, jour: str, creneau: str, utilisateur: str) -> bool:
        """Ajoute une réservation si pas de conflit. Retourne True si succès."""
        if not salle.est_disponible():
            print(f"❌ La salle {salle.nom} est indisponible.")
            return False

        if self.detecter_conflit(salle, jour, creneau):
            print(f"❌ Conflit détecté : {salle.nom} déjà réservée le {jour} à {creneau}.")
            return False

        nouvelle_reservation = Reservation(
            id=len(self.reservations) + 1,
            salle=salle,
            jour=jour,
            creneau=creneau,
            utilisateur=utilisateur
        )
        self.reservations.append(nouvelle_reservation)
        print(f"✅ Réservation confirmée : {salle.nom} le {jour} à {creneau}.")
        return True

    def afficher_planning(self):
        """Affiche toutes les réservations."""
        if not self.reservations:
            print("Aucune réservation enregistrée.")
            return
        print("\n--- PLANNING DES RÉSERVATIONS ---")
        for r in self.reservations:
            print(r)
        print("---------------------------------\n")