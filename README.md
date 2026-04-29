# Système de Réservation de Salles

Projet réalisé dans le cadre du cours de Programmation Python (Niveau L2).  
Approche : Apprentissage Par Projet (APP).

## Description
Planning interactif pour gérer les ressources d'une université (salles, projecteurs)
avec détection de conflits horaires.

## Équipe
- Étudiant 1 : SALIFOU Sabi Fawaz
- Étudiant 2 : YAHA Sandrine

---

## Bloc 2 — Workflow & Fondations

### Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Lancer le module

```bash
python src\data_structures.py
```

### Structures de données utilisées

| Structure | Usage dans le projet                      |
|-----------|-------------------------------------------|
| `dict`    | Catalogue des salles et leurs attributs   |
| `list`    | Créneaux horaires, réservations           |
| `tuple`   | Jours ouvrés (données immuables)          |
| `set`     | Équipements uniques disponibles           |

---

## Bloc 3 — Architecture (POO)

### Classes créées

| Classe | Fichier | Rôle |
|--------|---------|------|
| `Salle` | `src/models.py` | Représente une salle de l'université |
| `Reservation` | `src/models.py` | Représente une réservation de salle |
| `Planning` | `src/planning.py` | Gère les réservations et détecte les conflits |

### Lancer le menu interactif

```bash
python main.py
```

### Fonctionnalités disponibles

- Afficher toutes les salles et leur statut
- Faire une réservation (choix salle, jour, créneau, email)
- Détecter automatiquement les conflits horaires
- Afficher le planning complet des réservations

### Concepts POO appliqués

| Concept | Utilisation |
|---------|-------------|
| Encapsulation | Attributs privés gérés via `__init__` |
| Méthodes | `est_disponible()`, `ajouter_reservation()`, `detecter_conflit()` |
| `__str__` | Affichage lisible de chaque objet |
| Composition | `Reservation` contient un objet `Salle` |