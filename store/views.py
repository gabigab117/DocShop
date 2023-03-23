import stripe
import environ
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Shopper, ShippingAddress
from shop import settings
from shop.settings import BASE_DIR
from .models import Product, Cart, Order
from .forms import OrderForm
from pprint import pprint


environ.Env.read_env(BASE_DIR / "shop/.env")
stripe.api_key = settings.STRIPE_API_KEY


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', context={"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', context={"product": product})


def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    # le panier : s'il n'existe pas il est créé, sinon on le récupère
    cart, _ = Cart.objects.get_or_create(user=user)
    # regarde si on a un objet order qui correspond à notre utilisateur et si le produit correspond à product
    # ordered = false car on cible article pas déjà été commandé. On va recréer un article et pas modifier
    # l'existant True.
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)
    # si le produit n'était pas dans le panier et qu'il est créé
    if created:
        cart.orders.add(order)
        cart.save()
        # si déjà dans le panier
    else:
        order.quantity += 1
        order.save()
    return redirect(reverse("store:product", kwargs={"slug": slug}))


'''
get_or_create retourne deux choses : l'objet en question qu'il ai été créé ou qu'il existe déjà et aussi
une autre variable pour savoir si l'objet a été créé ou non.
'''


def cart(request):
    orders = Order.objects.filter(user=request.user, ordered=False)
    # si je n'ai pas d'articles en cours de commande
    if orders.count() == 0:
        return redirect('index')
    # formset auquel on précise le modele et le formulaire. extra 0 car je ne veux pas afficher des formulaires vierge
    # un formset car on a potentiellement plusieurs forms sur la mm page car peut-être plusieurs articles
    # je l'attribue à une variable ce qui me permet de créer une class.
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    # puis on va créer une instance
    # je veux récupérer uniquement les articles dans le panier de l'utilisateur
    formset = OrderFormSet(queryset=orders)
    return render(request, "store/cart.html", context={"forms": formset})


def update_quantities(request):
    # on va utiliser notre form set de la vue cart
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    # puis on récupère les données dans la requete POST (dictionnaire)
    formset = OrderFormSet(request.POST, queryset=Order.objects.filter(user=request.user, ordered=False))
    # comme d'hab je vérifie la validité
    if formset.is_valid():
        # je save
        formset.save()

    return redirect('store:cart')


def delete_cart(request):
    # récupère le panier
    # cart = request.user.cart
    if cart := request.user.cart:
        # la logique se retrouve directement dans la méthode delete du modele cart
        cart.delete()

    return redirect('index')


'''
J'ai utilise un walrus := qui permet de faire deux choses en une ligne
'''


def create_checkout_session(request):
    # récupère le panier
    cart = request.user.cart
    # compréhension de liste avec un dictionnaire (id + qté)
    line_items = [{"price": order.product.stripe_id,
                   "quantity": order.quantity} for order in cart.orders.all()]

    checkout_data = {
        "locale": "fr",
        "line_items": line_items,
        "mode": 'payment',
        # voir ds la doc. On passe un dico avec une liste de pays autorisés
        "shipping_address_collection": {"allowed_countries": ["FR", "BE"]},
        # il faut une url absolue car je suis sur Stripe à ce moment-là
        "success_url": request.build_absolute_uri(reverse('checkout-success')),
        "cancel_url": 'http://127.0.0.1:8000',
    }
    # une condition pour savoir si on a déjà un stripe_id pour notre user
    if request.user.stripe_id:
        checkout_data["customer"] = request.user.stripe_id
    else:
        checkout_data["customer_email"] = request.user.email
        # créer le client dans stripe la première fois
        checkout_data["customer_creation"] = "always"
    # tout ce que j'avais ici je l'ai passé à checkout_data en dictionnaire
    # on va utiliser l'unpacking
    session = stripe.checkout.Session.create(**checkout_data)

    return redirect(session.url, code=303)


def checkout_success(request):
    return render(request, "store/success.html")


env = environ.Env()


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = env("endpoint_secret")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # on veut récupérer l'évènement checkout.session.completed, il s'agit d'un dico
    if event['type'] == "checkout.session.completed":
        # dans event on a un objet qui permet de récup mail user produits acheté etc ds data object
        data = event['data']['object']
        pprint(data)
        try:
            user = get_object_or_404(Shopper, email=data['customer_details']['email'])
            # dans object (voir var data) on a l'email
        except KeyError:
            return HttpResponse("Invalid user email", status=404)

        # deux fonctions du dessous
        complete_order(data=data, user=user)
        save_shipping_adress(data=data, user=user)

        return HttpResponse(status=200)

    # Passed signature verification
    return HttpResponse(status=200)


# pas de requête ici on créer une fonction qui sera retournée dans la vue stripe_webhook
def complete_order(data, user):
    user.stripe_id = data['customer']
    user.cart.delete()
    # faire un save pour le stripe_id
    user.save()

    # 200 pour indiquer que le paiement a été procéssé correctement
    return HttpResponse(status=200)


def save_shipping_adress(data, user):
    """
   "shipping_details": {
    "address": {
      "city": "60650 - ONS EN BRAY",
      "country": "FR",
      "line1": "5 rue xxxxxx",
      "line2": null,
      "postal_code": "60650",
      "state": ""
    },
    "name": "GABRIEL TROUV\u00c9"
    """
    try:
        address = data["shipping_details"]["address"]
        name = data["shipping_details"]["name"]
        city = address["city"]
        country = address["country"]
        line1 = address["line1"]
        line2 = address["line2"]
        zip_code = address["postal_code"]
    except KeyError:
        return HttpResponse(status=400)

    ShippingAddress.objects.get_or_create(user=user,
                                          name=name,
                                          city=city,
                                          country=country.lower(),
                                          address_1=line1,
                                          # si line2 est none je mets plutot un str vide
                                          address_2=line2 or "",
                                          zip_code=zip_code)
    return HttpResponse(status=200)
