from django.test import TestCase
from store.models import Product


class ProductTest(TestCase):
    # vérifier si le slug est correctement généré
    def test_product_slug_is_automatically_generated(self):
        self.product = Product.objects.create(
            name="Sneakers Docstring",
            price=10,
            stock=10,
            description="De superbes godasses",
        )
        # on utilise les assert pour faire des vérif
        # vérifier une égalité slug du produit et une str
        self.assertEqual(self.product.slug, "sneakers-docstring")
