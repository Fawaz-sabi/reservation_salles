# src/data_structures.py
"""
Bloc 2 - Fondations : Types de données complexes
Projet : Système de Réservation de Salles
"""

# --- DICTIONNAIRES : Catalogue des salles ---
salles = {
    "A101": {"capacite": 30, "equipements": ["projecteur", "tableau"], "disponible": True},
    "B205": {"capacite": 50, "equipements": ["projecteur", "micro"], "disponible": True},
    "C010": {"capacite": 10, "equipements": ["tableau"], "disponible": False},
}

# --- LISTES : Créneaux horaires possibles ---
creneaux_disponibles = ["08:00-10:00", "10:00-12:00", "14:00-16:00", "16:00-18:00"]

# --- TUPLES : Jours ouvrés (immuable) ---
JOURS_OUVRES = ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi")

# --- ENSEMBLES (sets) : Équipements uniques disponibles ---
tous_equipements = set()
for salle in salles.values():
    tous_equipements.update(salle["equipements"])

# --- LISTE DE DICTS : Réservations en cours ---
reservations = [
    {
        "id": 1,
        "salle": "A101",
        "jour": "Lundi",
        "creneau": "08:00-10:00",
        "utilisateur": "dupont@univ.fr"
    },
]


def afficher_salles_disponibles(salles: dict) -> list:
    """Retourne la liste des salles disponibles."""
    return [code for code, info in salles.items() if info["disponible"]]


def chercher_salle_par_capacite(salles: dict, capacite_min: int) -> list:
    """Retourne les salles avec une capacité >= capacite_min."""
    return [
        code for code, info in salles.items()
        if info["capacite"] >= capacite_min
    ]


def detecter_conflit(reservations: list, salle: str, jour: str, creneau: str) -> bool:
    """Détecte si une réservation existe déjà pour ce créneau."""
    return any(
        r["salle"] == salle and r["jour"] == jour and r["creneau"] == creneau
        for r in reservations
    )


if __name__ == "__main__":
    print("Salles disponibles :", afficher_salles_disponibles(salles))
    print("Salles >= 30 places :", chercher_salle_par_capacite(salles, 30))
    print("Equipements uniques :", tous_equipements)
    print("Conflit A101/Lundi/08:00 :", detecter_conflit(reservations, "A101", "Lundi", "08:00-10:00"))