from django.test import TestCase
from django.urls import reverse

from accounts.models import Shopper
from store.models import Product, Cart, Order


class ProductTest(TestCase):
    # créer une instance de mon modèle dans la méthode setUp
    def setUp(self) -> None:
        self.product = Product.objects.create(
            name="Sneakers Docstring",
            price=10,
            stock=10,
            description="De superbes godasses",
        )
    # vérifier si le slug est correctement généré

    def test_product_slug_is_automatically_generated(self):
        # on utilise les assert pour faire des vérif
        # vérifier une égalité slug du produit et une str
        self.assertEqual(self.product.slug, "sneakers-docstring")

    # tester l'url absolue vers un produit get_absolute_url
    def test_product_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), reverse("store:product", kwargs={"slug": self.product.slug}))


class CartTest(TestCase):
    def setUp(self):
        user = Shopper.objects.create(email="test@gmail.com",
                                      password="123456")
        product = Product.objects.create(name="Sneakers Docstring")
        self.cart = Cart.objects.create(user=user)
        order = Order.objects.create(user=user,
                                     product=product)
        self.cart.orders.add(order)
        self.cart.save()

    def test_orders_changed_when_cart_is_deleted(self):
        # récupérer les pk ds une liste
        orders_pk = [order.pk for order in self.cart.orders.all()]
        self.cart.delete()
        for order_pk in orders_pk:
            order = Order.objects.get(pk=order_pk)
            # je regarde si ordered_date a une valeur
            self.assertIsNotNone(order.ordered_date)
            # si ordered est à True
            self.assertTrue(order.ordered)
