from django.test import TestCase
from django.urls import reverse

from store.models import Product


class StoreTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="t shirt",
            price=10,
            stock=10,
            description="beau t shirt"
        )

    # je veux m'assurer que mon produit va bien s'afficher dans la page d'accueil
    def test_products_are_shown_on_index_page(self):
        # pour tester ça on va utiliser un client. ça permet de faire des requêtes
        # rappel, avec reverse on récupère une url depuis son nom
        resp = self.client.get(reverse("index"))
        # on vérifie que le status est de 200
        self.assertEqual(resp.status_code, 200)
        # on vérifie que le nom du produit est affiché sur la page d'accueil
        # le nom du produit in contenu de la page, c a d dans le code html (convertir en str)
        self.assertIn(self.product.name, str(resp.content))

    def test_connexion_link_shown_when_user_not_connected(self):
        resp = self.client.get(reverse("index"))
        # connexion est dans ma page index ?
        self.assertIn("Connexion", str(resp.content))

    def test_redirect_when_anonymous_user_access_cart_view(self):
        resp = self.client.get(reverse("store:cart"))
        # 302 est une vue de redirection
        self.assertEqual(resp.status_code, 302)
        # vérifier si c'est la bonne vue "account/login/?next=/store/cart/"
        self.assertRedirects(resp, f"{reverse('accounts:login')}?next={reverse('store:cart')}", status_code=302)
