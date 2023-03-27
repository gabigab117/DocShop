from django.test import TestCase
from accounts.models import Shopper
from store.models import Product


class UserTest(TestCase):
    def setUp(self):
        Product.objects.create(
            name="T shirt pourrave",
            price=10,
            stock=10,
            description="Un Tshirt de mer..."
        )
        # on récupère dans self.user car on va utiliser dans add to cart
        self.user: Shopper = Shopper.objects.create_user(
            email="gab@gab.com",
            password="123456"
        )

    def test_add_to_cart(self):
        self.user.add_to_cart(slug="t-shirt-pourrave")
        # self.user.cart.orders retourne un queryset (manytomany). On compte le nombre d'éléments
        self.assertEqual(self.user.cart.orders.count(), 1)
        self.assertEqual(self.user.cart.orders.first().product.slug, "t-shirt-pourrave")
        self.user.add_to_cart(slug="t-shirt-pourrave")
        # vérifie qu'on a tjours qu'une order
        self.assertEqual(self.user.cart.orders.count(), 1)
        # vérifie la quantité
        self.assertEqual(self.user.cart.orders.first().quantity, 2)


'''
Ici je préfixe user avec self. comme ça je peux le re utiliser dans toutes les méthodes de ma classe. C'est à dire tous
les tests de ma classe.
'''