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
    message = ""

    if request.method == "POST":
        form = MoveForm(request.POST, instance=personnage)
        if form.is_valid():

            personnage_temp = form.save(commit=False)
            nouveau_lieu = personnage_temp.lieu


            if nouveau_lieu.est_disponible():
                personnage_temp.transition_etat()

                # Mise à jour des lieux
                if ancien_lieu:
                    ancien_lieu.retirer_personnage()
                nouveau_lieu.ajouter_personnage()

                # Sauvegarder les modifications dans la base de données
                personnage_temp.save()

                # Rediriger vers la page de détails du personnage après le changement
                return redirect('personnage_detail', id_personnage=id_personnage)
            else:
                # Si le lieu n'est pas disponible, afficher un message d'avertissement
                message = f"Le lieu '{nouveau_lieu.nom}' est plein. Impossible de déplacer {personnage.nom}."
    else:
        form = MoveForm(instance=personnage)

    return render(request, 'blog/personnage_detail.html', {
        'personnage': personnage,
        'lieu': ancien_lieu,
        'form': form,
        'message': message
    })