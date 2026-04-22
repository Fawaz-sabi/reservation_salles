# main.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models import Salle, Reservation
from planning import Planning

# --- Données initiales ---
salles = {
    "A101": Salle("A101", 30, ["projecteur", "tableau"]),
    "B205": Salle("B205", 50, ["projecteur", "micro"]),
    "C010": Salle("C010", 10, ["tableau"], disponible=False),
}

JOURS_OUVRES = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
CRENEAUX = ["08:00-10:00", "10:00-12:00", "14:00-16:00", "16:00-18:00"]

planning = Planning()


def afficher_menu():
    print("\n========================================")
    print("   SYSTÈME DE RÉSERVATION DE SALLES")
    print("========================================")
    print("1. Afficher toutes les salles")
    print("2. Faire une réservation")
    print("3. Afficher le planning")
    print("4. Quitter")
    print("========================================")


def afficher_salles():
    print("\n--- LISTE DES SALLES ---")
    for salle in salles.values():
        print(salle)


def choisir_salle():
    print("\nSalles disponibles :")
    for code, salle in salles.items():
        statut = "✅" if salle.est_disponible() else "❌"
        print(f"  {statut} {code} | Capacité : {salle.capacite}")
    code = input("Entrez le code de la salle : ").strip().upper()
    if code not in salles:
        print("❌ Salle introuvable.")
        return None
    return salles[code]


def choisir_jour():
    print("\nJours disponibles :")
    for i, jour in enumerate(JOURS_OUVRES, 1):
        print(f"  {i}. {jour}")
    choix = input("Choisissez un jour (1-5) : ").strip()
    if not choix.isdigit() or int(choix) not in range(1, 6):
        print("❌ Choix invalide.")
        return None
    return JOURS_OUVRES[int(choix) - 1]


def choisir_creneau():
    print("\nCréneaux disponibles :")
    for i, creneau in enumerate(CRENEAUX, 1):
        print(f"  {i}. {creneau}")
    choix = input("Choisissez un créneau (1-4) : ").strip()
    if not choix.isdigit() or int(choix) not in range(1, 5):
        print("❌ Choix invalide.")
        return None
    return CRENEAUX[int(choix) - 1]


def faire_reservation():
    print("\n--- NOUVELLE RÉSERVATION ---")
    salle = choisir_salle()
    if not salle:
        return
    jour = choisir_jour()
    if not jour:
        return
    creneau = choisir_creneau()
    if not creneau:
        return
    utilisateur = input("Entrez votre email : ").strip()
    if not utilisateur:
        print("❌ Email invalide.")
        return
    planning.ajouter_reservation(salle, jour, creneau, utilisateur)


# --- Boucle principale ---
while True:
    afficher_menu()
    choix = input("Votre choix (1-4) : ").strip()

    if choix == "1":
        afficher_salles()
    elif choix == "2":
        faire_reservation()
    elif choix == "3":
        planning.afficher_planning()
    elif choix == "4":
        print("\nAu revoir ! 👋")
        break
    else:
        print("❌ Choix invalide, entrez un nombre entre 1 et 4.")