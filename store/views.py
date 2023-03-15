import stripe
import environ
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Shopper
from shop import settings
from shop.settings import BASE_DIR
from .models import Product, Cart, Order


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
    return redirect(reverse("product", kwargs={"slug": slug}))


'''
get_or_create retourne deux choses : l'objet en question qu'il ai été créé ou qu'il existe déjà et aussi
une autre variable pour savoir si l'objet a été créé ou non.
'''


def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, "store/cart.html", context={"orders": cart.orders.all()})


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

    session = stripe.checkout.Session.create(
        locale="fr",
        line_items=line_items,
        mode='payment',
        # il faut une url absolue car je suis sur Stripe à ce moment-là
        success_url=request.build_absolute_uri(reverse('checkout-success')),
        cancel_url='http://127.0.0.1:8000',
    )

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
        return complete_order(data)

    # Passed signature verification
    return HttpResponse(status=200)


# pas de requête ici on créer une fonction qui sera retournée dans la vue stripe_webhook
def complete_order(data):
    try:
        # dans object (voir var data) on a l'email
        user_email = data['customer_details']['email']
    except KeyError:
        return HttpResponse("Invalid user email", status=404)

    user = get_object_or_404(Shopper, email=user_email)
    user.cart.delete()
    # 200 pour indiquer que le paiement a été procéssé correctement
    return HttpResponse(status=200)
