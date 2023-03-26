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
        self.user: Shopper = Shopper.objects.create_user(
            email="gab@gab.com",
            password="123456"
        )

    def add_to_cart(self):
        self.user.add_to_cart(slug="t-shirt-pourrave")
        self.assertEqual(self.user.cart.orders.count(), 1)
        self.assertEqual(self.user.cart.orders.first().product.slug, "t-shirt-pourrave")
