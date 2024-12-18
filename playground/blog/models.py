from django.db import models

class Lieu(models.Model):
    id_equip = models.CharField(max_length=100, primary_key=True)
    nom = models.CharField(max_length=100)  # Nom du lieu (ex: Auberge)
    capacite = models.IntegerField()  # Capacité maximale du lieu
    nombre_actuel = models.IntegerField(default=0)  # Nombre actuel de personnages présents dans ce lieu
    photo = models.CharField(max_length=200)  # Lien vers une image du lieu

    def est_disponible(self):
        """Vérifie si le lieu a de la place disponible."""
        return self.nombre_actuel < self.capacite

    def ajouter_personnage(self):
        """Ajoute un personnage au lieu, si possible."""
        if self.est_disponible():
            self.nombre_actuel += 1
            self.save()

    def retirer_personnage(self):
        """Retire un personnage du lieu, si possible."""
        if self.nombre_actuel > 0:
            self.nombre_actuel -= 1
            self.save()

    def __str__(self):
        return self.nom

    @property
    def personnage_set(self):
        """Retourne les personnages associés à ce lieu."""
        return Personnage.objects.filter(lieu=self)

class Personnage(models.Model):

    id_personnage = models.CharField(max_length=100, primary_key=True)
    nom = models.CharField(max_length=100)
    etat = models.CharField(
        max_length=20,
        choices=[
            ('Fatigué', 'Fatigué'),
            ('Rassasié', 'Rassasié'),
            ('Entraîné', 'Entraîné'),
            ('Stratégique', 'Stratégique'),
            ('Prêt', 'Prêt')
        ]
    )
    type_personnage = models.CharField(max_length=20)
    photo = models.CharField(max_length=200)
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)


    def changer_etat(self, nouvel_etat, nouveau_lieu):
        if nouveau_lieu.est_disponible():
            self.etat = nouvel_etat
            if self.lieu:
                self.lieu.retirer_personnage()
            nouveau_lieu.ajouter_personnage()
            self.lieu = nouveau_lieu
            self.save()


    def transition_etat(self):
        transitions = {
            'Fatigué': ('Rassasié', 'Auberge'),
            'Rassasié': ('Entraîné', 'Forêt Enchantée'),
            'Entraîné': ('Stratégique', 'Tour de Magie'),
            'Stratégique': ('Prêt', 'Château'),
            'Prêt': ('Fatigué', 'Caverne des Dragons')
        }

        if self.etat in transitions:
            nouvel_etat, nom_lieu = transitions[self.etat]
            nouveau_lieu = Lieu.objects.get(nom=nom_lieu)
            self.changer_etat(nouvel_etat, nouveau_lieu)

    def __str__(self):
        return self.nom