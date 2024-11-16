from django.shortcuts import render, get_object_or_404, redirect
from .models import Personnage, Lieu
from .forms import MoveForm

def post_list(request):
    personnages = Personnage.objects.all()
    lieux=Lieu.objects.all()
    return render(request, 'blog/post_list.html', {'personnages': personnages,'lieux': lieux})


def personnage_detail(request, id_personnage):
    personnage = get_object_or_404(Personnage, id_personnage=id_personnage)
    ancien_lieu = personnage.lieu

    if request.method == "POST":
        form = MoveForm(request.POST, instance=personnage)
        if form.is_valid():
            # Sauvegarder les informations de l'ancien lieu
            ancien_lieu = get_object_or_404(Lieu, id_equip=personnage.lieu.id_equip)

            # Mettre à jour l'occupation du lieu actuel à "libre"
            ancien_lieu.retirer_personnage()

            # Sauvegarder le nouvel état du personnage et son nouveau lieu
            nouveau_lieu = form.cleaned_data['lieu']

            # Vérifie la disponibilité du nouveau lieu avant d'effectuer la transition
            if nouveau_lieu.est_disponible():
                # Mise à jour de l'état du personnage selon le nouveau lieu
                personnage.transition_etat(nouveau_lieu)

                # Mettre à jour l'occupation du nouveau lieu à "occupé"
                nouveau_lieu.ajouter_personnage()

                # Redirige vers la page de détails du personnage après le changement
                return redirect('personnage_detail', id_personnage=id_personnage)
    else:
        form = MoveForm(instance=personnage)

    return render(request, 'blog/personnage_detail.html', {
        'personnage': personnage,
        'lieu': ancien_lieu,
        'form': form
    })