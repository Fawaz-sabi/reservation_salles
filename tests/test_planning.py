# tests/test_planning.py
"""
Bloc 5 - Tests unitaires avec Pytest
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Salle, Reservation, SalleIndisponibleError, ConflitReservationError, ReservationIntrouvableError
from planning import Planning
import pytest


# --- Fixtures ---
@pytest.fixture
def salle_disponible():
    return Salle("Solidarité R+1", 30, ["projecteur", "tableau"])

@pytest.fixture
def salle_indisponible():
    return Salle("Salle 17", 10, ["tableau"], disponible=False)

@pytest.fixture
def planning_vide():
    return Planning()


# --- Tests classe Salle ---
def test_salle_disponible(salle_disponible):
    assert salle_disponible.est_disponible() == True

def test_salle_indisponible(salle_indisponible):
    assert salle_indisponible.est_disponible() == False

def test_salle_str(salle_disponible):
    assert "Solidarité R+1" in str(salle_disponible)
    assert "30" in str(salle_disponible)


# --- Tests classe Planning ---
def test_ajouter_reservation(planning_vide, salle_disponible):
    planning_vide.ajouter_reservation(salle_disponible, "Lundi", "08:00-10:00", "dupont@univ.fr")
    assert len(planning_vide.reservations) == 1

def test_detecter_conflit(planning_vide, salle_disponible):
    planning_vide.ajouter_reservation(salle_disponible, "Lundi", "08:00-10:00", "dupont@univ.fr")
    assert planning_vide.detecter_conflit(salle_disponible, "Lundi", "08:00-10:00") == True

def test_pas_de_conflit(planning_vide, salle_disponible):
    planning_vide.ajouter_reservation(salle_disponible, "Lundi", "08:00-10:00", "dupont@univ.fr")
    assert planning_vide.detecter_conflit(salle_disponible, "Mardi", "10:00-12:00") == False


# --- Tests exceptions ---
def test_salle_indisponible_exception(planning_vide, salle_indisponible):
    with pytest.raises(SalleIndisponibleError):
        planning_vide.ajouter_reservation(salle_indisponible, "Lundi", "08:00-10:00", "dupont@univ.fr")

def test_conflit_exception(planning_vide, salle_disponible):
    planning_vide.ajouter_reservation(salle_disponible, "Lundi", "08:00-10:00", "dupont@univ.fr")
    with pytest.raises(ConflitReservationError):
        planning_vide.ajouter_reservation(salle_disponible, "Lundi", "08:00-10:00", "martin@univ.fr")

def test_supprimer_reservation_introuvable(planning_vide):
    with pytest.raises(ReservationIntrouvableError):
        planning_vide.supprimer_reservation(999)