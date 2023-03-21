from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import UserForm
from accounts.models import ShippingAddress

User = get_user_model()


def signup(request):
    if request.method == "POST":
        # traiter le formulaire
        # le nom des clés dans le dictionnaire sont définits par name="" dans la balise html de l'input
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(email=email, password=password)
        login(request, user)
        return redirect('index')

    return render(request, "accounts/signup.html")


def logout_user(request):
    logout(request)
    return redirect('index')


def login_user(request):
    if request.method == "POST":
        # connecter l'user
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')

    return render(request, "accounts/login.html")


@login_required
def profil(request):
    if request.method == "POST":
        # vérifier si le bon mdp est entré
        is_valid = authenticate(email=request.POST.get("email"), password=request.POST.get("password"))
        if is_valid:
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.save()
        else:
            # on va passer par messages, ils sont associés à la session de l'utilisateur, donc on peut les transporter
            # mais si je boucle sur les messages ils sont supprimés ?
            # même pas besoin de passer par le context. Une variable dans le html
            messages.add_message(request, messages.ERROR, "le mot de passe n'est pas valide.")

        return redirect("profil")

    # les valeurs initiales, utiliser model_to_dict() Mais on exclu le champ password
    form = UserForm(initial=model_to_dict(request.user, exclude="password"))
    # récupérer toutes les adresses de l'utilisateur, mettre le shipping en minuscule
    addresses = request.user.addresses.all()

    return render(request, "accounts/profil.html", context={'form': form,
                                                            "addresses": addresses})


@login_required
def set_default_shipping_address(request, pk):
    # j'ajoute une annotation de type
    address: ShippingAddress = get_object_or_404(ShippingAddress, pk=pk)
    address.set_default()
    return redirect('profil')
