from django import forms
from .models import Personnage, Lieu

class MoveForm(forms.ModelForm):
    class Meta:
        model = Personnage
        fields = ('lieu',)  # Champ pour changer le lieu du personnage
        labels = {
            'lieu': "Nouveau Lieu",
        }
        widgets = {
            'lieu': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def save(self, commit=True):
        personnage = super().save(commit=False)
        personnage.transition_etat(personnage.etat)
        if commit:
            personnage.save()
        return personnage