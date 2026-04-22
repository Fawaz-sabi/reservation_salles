class Salle:
    def __init__(self, nom, capacite):
        self.nom = nom
        self.capacite = capacite

    def afficher_infos(self):
        print("Nom de la salle  :", self.nom)
        print("Capacité :", self.capacite, "places")


class Ressource:
    def __init__(self, nom):
        self.nom = nom

    def afficher_ressource(self):
        print("Ressource :", self.nom)


class Projecteur(Ressource):
    def __init__(self, nom):
        super().__init__(nom)


class Reservation:
    def __init__(self, salle, date, heure_debut, heure_fin):
        self.salle = salle
        self.date = date
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin

    def afficher_reservation(self):
        print("Réservation de", self.salle.nom)
        print("Date :", self.date)
        print("Heure début :", self.heure_debut)
        print("Heure fin :", self.heure_fin)
