# src/planning.py
"""
Bloc 5 - Qualité
Classe Planning avec gestion des exceptions
"""

from models import Salle, Reservation
from models import SalleIndisponibleError, ConflitReservationError, ReservationIntrouvableError


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
        """Ajoute une réservation si pas de conflit.
        
        Raises:
            SalleIndisponibleError: Si la salle est indisponible.
            ConflitReservationError: Si un conflit horaire est détecté.
        """
        if not salle.est_disponible():
            raise SalleIndisponibleError(f"La salle {salle.nom} est indisponible.")

        if self.detecter_conflit(salle, jour, creneau):
            raise ConflitReservationError(
                f"Conflit détecté : {salle.nom} déjà réservée le {jour} à {creneau}."
            )

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

    def supprimer_reservation(self, reservation_id: int):
        """Supprime une réservation par son ID.
        
        Raises:
            ReservationIntrouvableError: Si l'ID n'existe pas.
        """
        reservation = next((r for r in self.reservations if r.id == reservation_id), None)
        if not reservation:
            raise ReservationIntrouvableError(f"Réservation #{reservation_id} introuvable.")
        self.reservations.remove(reservation)
        return reservation

    def afficher_planning(self):
        """Affiche toutes les réservations."""
        if not self.reservations:
            print("Aucune réservation enregistrée.")
            return
        print("\n--- PLANNING DES RÉSERVATIONS ---")
        for r in self.reservations:
            print(r)
        print("---------------------------------\n")