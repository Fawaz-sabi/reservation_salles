# src/database.py
"""
Bloc 4 - Persistance
Gestion de la base de données SQLite
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'reservation.db')


def init_db():
    """Crée les tables si elles n'existent pas encore."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salles (
            nom TEXT PRIMARY KEY,
            capacite INTEGER NOT NULL,
            equipements TEXT NOT NULL,
            disponible INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            salle_nom TEXT NOT NULL,
            jour TEXT NOT NULL,
            creneau TEXT NOT NULL,
            utilisateur TEXT NOT NULL,
            FOREIGN KEY (salle_nom) REFERENCES salles(nom)
        )
    ''')

    conn.commit()
    conn.close()


def sauvegarder_salle(salle):
    """Sauvegarde une salle dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO salles (nom, capacite, equipements, disponible)
        VALUES (?, ?, ?, ?)
    ''', (
        salle.nom,
        salle.capacite,
        ','.join(salle.equipements),
        int(salle.disponible)
    ))

    conn.commit()
    conn.close()


def sauvegarder_reservation(reservation):
    """Sauvegarde une réservation dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO reservations (salle_nom, jour, creneau, utilisateur)
        VALUES (?, ?, ?, ?)
    ''', (
        reservation.salle.nom,
        reservation.jour,
        reservation.creneau,
        reservation.utilisateur
    ))

    conn.commit()
    conn.close()


def charger_reservations(salles: dict) -> list:
    """Charge toutes les réservations depuis la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT id, salle_nom, jour, creneau, utilisateur FROM reservations')
    rows = cursor.fetchall()
    conn.close()

    from models import Reservation
    reservations = []
    for row in rows:
        id_, salle_nom, jour, creneau, utilisateur = row
        if salle_nom in salles:
            r = Reservation(id_, salles[salle_nom], jour, creneau, utilisateur)
            reservations.append(r)
    return reservations


def supprimer_reservation(reservation_id: int):
    """Supprime une réservation par son ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM reservations WHERE id = ?', (reservation_id,))

    conn.commit()
    conn.close()
    print(f"✅ Réservation #{reservation_id} supprimée.")