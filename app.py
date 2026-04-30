# app.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, render_template, request, redirect, url_for, flash
from models import Salle, SalleIndisponibleError, ConflitReservationError, ReservationIntrouvableError
from planning import Planning
from database import init_db, sauvegarder_salle, sauvegarder_reservation, charger_reservations, supprimer_reservation

app = Flask(__name__)
app.secret_key = "universite_parakou_2026"

init_db()

salles = {
    "Solidarité R+1": Salle("Solidarité R+1", 30, ["projecteur", "tableau"]),
    "Amphi 1000":     Salle("Amphi 1000", 50, ["projecteur", "micro"]),
    "Salle 17":       Salle("Salle 17", 10, ["tableau"], disponible=False),
}

for salle in salles.values():
    sauvegarder_salle(salle)

JOURS_OUVRES = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]

planning = Planning()
planning.reservations = charger_reservations(salles)


def email_autorise(email: str) -> bool:
    """Seuls les emails @univ-parakou.bj sont autorisés."""
    return email.strip().endswith("@univ-parakou.bj")


def valider_creneau(creneau: str) -> bool:
    """Vérifie que le créneau est au format HH:MM-HH:MM."""
    import re
    return bool(re.match(r'^\d{2}:\d{2}-\d{2}:\d{2}$', creneau.strip()))


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        salles=salles,
        jours=JOURS_OUVRES,
        reservations=planning.reservations
    )


@app.route("/reserver", methods=["POST"])
def reserver():
    salle_nom   = request.form.get("salle", "").strip()
    jour        = request.form.get("jour", "").strip()
    creneau     = request.form.get("creneau", "").strip()
    utilisateur = request.form.get("email", "").strip()

    # Vérification champs vides
    if not all([salle_nom, jour, creneau, utilisateur]):
        flash("Veuillez remplir tous les champs.", "danger")
        return redirect(url_for("index"))

    # Vérification email universitaire
    if not email_autorise(utilisateur):
        flash("❌ Seuls les emails @univ-parakou.bj sont autorisés à réserver.", "danger")
        return redirect(url_for("index"))

    # Vérification format créneau
    if not valider_creneau(creneau):
        flash("❌ Format de créneau invalide. Utilisez le format HH:MM-HH:MM (ex: 08:00-10:00).", "danger")
        return redirect(url_for("index"))

    salle = salles.get(salle_nom)
    if not salle:
        flash("Salle introuvable.", "danger")
        return redirect(url_for("index"))

    # Vérification salle non réservable
    if not salle.est_disponible():
        flash(f"❌ La salle {salle_nom} n'est pas réservable.", "danger")
        return redirect(url_for("index"))

    try:
        planning.ajouter_reservation(salle, jour, creneau, utilisateur)
        sauvegarder_reservation(planning.reservations[-1])
        flash(f"✅ Réservation confirmée : {salle_nom} — {jour} {creneau}", "success")
    except SalleIndisponibleError as e:
        flash(f"❌ {str(e)}", "danger")
    except ConflitReservationError:
        flash(f"⚠️ Ce créneau est déjà occupé : {salle_nom} est prise le {jour} de {creneau}. Choisissez un autre créneau.", "warning")

    return redirect(url_for("index"))


@app.route("/supprimer/<int:reservation_id>", methods=["POST"])
def supprimer(reservation_id):
    try:
        planning.supprimer_reservation(reservation_id)
        supprimer_reservation(reservation_id)
        flash(f"✅ Réservation #{reservation_id} supprimée.", "success")
    except ReservationIntrouvableError as e:
        flash(str(e), "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)