from django import forms
from .models import Personnage, Lieu

class MoveForm(forms.ModelForm):
    class Meta:
        model = Personnage
        fields = ('lieu',)
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
        personnage.transition_etat()
        if commit:
            personnage.save()
        return personnage