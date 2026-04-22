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