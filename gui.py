# gui.py
"""
Bloc 6 - Interface Graphique Tkinter
Système de Réservation de Salles
Université de Parakou - Bénin
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import tkinter as tk
from tkinter import ttk, messagebox

from models import Salle, SalleIndisponibleError, ConflitReservationError, ReservationIntrouvableError
from planning import Planning
from database import init_db, sauvegarder_salle, sauvegarder_reservation, charger_reservations, supprimer_reservation

# --- Initialisation ---
init_db()

salles = {
    "Solidarité R+1": Salle("Solidarité R+1", 30, ["projecteur", "tableau"]),
    "Amphi 1000":     Salle("Amphi 1000", 50, ["projecteur", "micro"]),
    "Salle 17":       Salle("Salle 17", 10, ["tableau"], disponible=False),
}

for salle in salles.values():
    sauvegarder_salle(salle)

JOURS_OUVRES = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
CRENEAUX = ["08:00-10:00", "10:00-12:00", "14:00-16:00", "16:00-18:00"]

planning = Planning()
planning.reservations = charger_reservations(salles)

# --- Couleurs ---
COULEUR_FOND        = "#FFFFFF"
COULEUR_HEADER      = "#003F7D"
COULEUR_SOUS_HEADER = "#0066CC"
COULEUR_BTN_RESERVER= "#28A745"
COULEUR_BTN_SUPPR   = "#DC3545"
COULEUR_TEXTE_CLAIR = "#FFFFFF"
COULEUR_TEXTE_SOMBRE= "#212529"
COULEUR_BORDURE     = "#DEE2E6"
COULEUR_LIGNE_PAIR  = "#F8F9FA"
COULEUR_LIGNE_IMPAIR= "#FFFFFF"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Système de Réservation de Salles — Université de Parakou")
        self.geometry("800x620")
        self.resizable(False, False)
        self.configure(bg=COULEUR_FOND)
        self._build_ui()
        self._actualiser_planning()

    def _build_ui(self):
        # ── HEADER ──────────────────────────────────────────
        header = tk.Frame(self, bg=COULEUR_HEADER, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="UNIVERSITÉ DE PARAKOU",
            font=("Helvetica", 13, "bold"),
            bg=COULEUR_HEADER, fg=COULEUR_TEXTE_CLAIR
        ).pack(pady=(12, 0))

        tk.Label(
            header,
            text="Système de Réservation de Salles",
            font=("Helvetica", 10),
            bg=COULEUR_HEADER, fg="#AED6F1"
        ).pack()

        # ── SOUS-HEADER ─────────────────────────────────────
        sous_header = tk.Frame(self, bg=COULEUR_SOUS_HEADER, height=4)
        sous_header.pack(fill="x")

        # ── BODY ────────────────────────────────────────────
        body = tk.Frame(self, bg=COULEUR_FOND)
        body.pack(fill="both", expand=True, padx=20, pady=15)

        # Colonne gauche : formulaire
        col_gauche = tk.Frame(body, bg=COULEUR_FOND)
        col_gauche.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(
            col_gauche,
            text="Nouvelle Réservation",
            font=("Helvetica", 12, "bold"),
            bg=COULEUR_FOND, fg=COULEUR_HEADER
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        champs = [("Salle :", "combo_salle"), ("Jour :", "combo_jour"), ("Créneau :", "combo_creneau")]
        valeurs = [list(salles.keys()), JOURS_OUVRES, CRENEAUX]

        for i, ((label, attr), vals) in enumerate(zip(champs, valeurs), 1):
            tk.Label(
                col_gauche, text=label,
                font=("Helvetica", 10),
                bg=COULEUR_FOND, fg=COULEUR_TEXTE_SOMBRE
            ).grid(row=i, column=0, sticky="w", pady=6)

            var = tk.StringVar()
            combo = ttk.Combobox(col_gauche, textvariable=var, values=vals,
                                 state="readonly", width=25)
            combo.grid(row=i, column=1, pady=6, padx=(10, 0))
            setattr(self, attr, combo)
            setattr(self, f"var_{attr.replace('combo_', '')}", var)

        # Email
        tk.Label(
            col_gauche, text="Email :",
            font=("Helvetica", 10),
            bg=COULEUR_FOND, fg=COULEUR_TEXTE_SOMBRE
        ).grid(row=4, column=0, sticky="w", pady=6)

        self.entry_email = tk.Entry(col_gauche, width=27, font=("Helvetica", 10),
                                    relief="solid", bd=1)
        self.entry_email.grid(row=4, column=1, pady=6, padx=(10, 0))

        # Bouton Réserver
        tk.Button(
            col_gauche,
            text="  ✔  Réserver  ",
            font=("Helvetica", 11, "bold"),
            bg=COULEUR_BTN_RESERVER, fg=COULEUR_TEXTE_CLAIR,
            activebackground="#218838",
            relief="flat", cursor="hand2",
            command=self._faire_reservation
        ).grid(row=5, column=1, sticky="e", pady=15)

        # Séparateur vertical
        tk.Frame(body, bg=COULEUR_BORDURE, width=1).pack(side="left", fill="y")

        # Colonne droite : planning
        col_droite = tk.Frame(body, bg=COULEUR_FOND)
        col_droite.pack(side="left", fill="both", expand=True, padx=(15, 0))

        tk.Label(
            col_droite,
            text="Planning des Réservations",
            font=("Helvetica", 12, "bold"),
            bg=COULEUR_FOND, fg=COULEUR_HEADER
        ).pack(anchor="w", pady=(0, 10))

        # Tableau avec colonnes
        colonnes = ("id", "salle", "jour", "creneau", "email")
        self.table = ttk.Treeview(col_droite, columns=colonnes, show="headings", height=12)

        self.table.heading("id",      text="#")
        self.table.heading("salle",   text="Salle")
        self.table.heading("jour",    text="Jour")
        self.table.heading("creneau", text="Créneau")
        self.table.heading("email",   text="Email")

        self.table.column("id",      width=30,  anchor="center")
        self.table.column("salle",   width=120, anchor="w")
        self.table.column("jour",    width=70,  anchor="center")
        self.table.column("creneau", width=90,  anchor="center")
        self.table.column("email",   width=150, anchor="w")

        # Style tableau
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading",
                        background=COULEUR_HEADER,
                        foreground=COULEUR_TEXTE_CLAIR,
                        font=("Helvetica", 10, "bold"))
        style.configure("Treeview", rowheight=28, font=("Helvetica", 10))
        style.map("Treeview", background=[("selected", COULEUR_SOUS_HEADER)])

        self.table.tag_configure("pair",   background=COULEUR_LIGNE_PAIR)
        self.table.tag_configure("impair", background=COULEUR_LIGNE_IMPAIR)

        scrollbar = ttk.Scrollbar(col_droite, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        # Bouton supprimer
        tk.Button(
            col_droite,
            text="  🗑  Supprimer la sélection  ",
            font=("Helvetica", 10),
            bg=COULEUR_BTN_SUPPR, fg=COULEUR_TEXTE_CLAIR,
            activebackground="#C82333",
            relief="flat", cursor="hand2",
            command=self._supprimer_reservation
        ).pack(anchor="e", pady=10)

        # ── FOOTER ──────────────────────────────────────────
        footer = tk.Frame(self, bg=COULEUR_HEADER, height=30)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Label(
            footer,
            text="Université de Parakou — Licence 2 Informatique — 2025/2026",
            font=("Helvetica", 8),
            bg=COULEUR_HEADER, fg="#AED6F1"
        ).pack(pady=6)

    def _faire_reservation(self):
        salle_nom = self.var_salle.get()
        jour      = self.var_jour.get()
        creneau   = self.var_creneau.get()
        email     = self.entry_email.get().strip()

        if not all([salle_nom, jour, creneau, email]):
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        salle = salles[salle_nom]
        try:
            planning.ajouter_reservation(salle, jour, creneau, email)
            sauvegarder_reservation(planning.reservations[-1])
            self._actualiser_planning()
            self.entry_email.delete(0, tk.END)
            messagebox.showinfo("Succès", f"Réservation confirmée !\n{salle_nom} — {jour} {creneau}")
        except SalleIndisponibleError as e:
            messagebox.showerror("Salle indisponible", str(e))
        except ConflitReservationError as e:
            messagebox.showerror("Conflit détecté", str(e))

    def _supprimer_reservation(self):
        selection = self.table.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une réservation.")
            return
        item = self.table.item(selection[0])
        reservation_id = int(item["values"][0])
        confirm = messagebox.askyesno("Confirmer", f"Supprimer la réservation #{reservation_id} ?")
        if confirm:
            try:
                planning.supprimer_reservation(reservation_id)
                supprimer_reservation(reservation_id)
                self._actualiser_planning()
                messagebox.showinfo("Succès", "Réservation supprimée.")
            except ReservationIntrouvableError as e:
                messagebox.showerror("Erreur", str(e))

    def _actualiser_planning(self):
        for row in self.table.get_children():
            self.table.delete(row)
        for i, r in enumerate(planning.reservations):
            tag = "pair" if i % 2 == 0 else "impair"
            self.table.insert("", tk.END, values=(
                r.id, r.salle.nom, r.jour, r.creneau, r.utilisateur
            ), tags=(tag,))


if __name__ == "__main__":
    app = App()
    app.mainloop()