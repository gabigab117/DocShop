from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Product, Cart, Order


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
    order, created = Order.objects.get_or_create(user=user, product=product)
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
