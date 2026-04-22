from models import Salle, Projecteur, Reservation

# Création d'une salle
salle1 = Salle("Salle Informatique", 30)

# Création d'un projecteur
proj1 = Projecteur("Projecteur Epson")

# Création d'une réservation
res1 = Reservation(salle1, "22/04/2026", "08:00", "10:00")

# Affichage
salle1.afficher_infos()
print()

proj1.afficher_ressource()
print()

res1.afficher_reservation()