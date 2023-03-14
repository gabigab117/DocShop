import stripe
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from shop import settings
from .models import Product, Cart, Order


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


@csrf_exempt
def stripe_webhook(request):
    payload = request.body

    print(payload)

    return HttpResponse(status=200)
