from django.test import TestCase
from accounts.models import Shopper
from django.urls import reverse


class StoreLoggedInTest(TestCase):
    def setUp(self):
        self.user = Shopper.objects.create_user(
            email="gab@gab.com",
            first_name="Patrick",
            last_name="smith",
            password="123456789"
        )

    def test_valid_login(self):
        data = {"email": "gab@gab.com", "password": "123456789"}
        resp = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(reverse('index'))
        self.assertIn("Mon profil", str(resp.content))

    def test_invalid_login(self):
        data = {"email": "gab@gab.com", "password": "1234"}
        resp = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "accounts/login.html")

    def test_profile_view(self):
        self.client.login(email="gab@gab.com",
                          password="123456789")
        resp = self.client.get(reverse('accounts:profil'))
        self.assertEqual(resp.status_code, 200)

    # def test_profile_not_change_because_wrong_password(self):
    #     self.client.login(
    #         email="gab@gab.com",
    #         password="123456789"
    #     )
    #
    #     data = {
    #         "email": "gab@gab.com",
    #         "password": "1234567",
    #         "first_name": "Patrick",
    #         "last_name": "Martin"
    #     }
    #     resp = self.client.post(reverse("accounts:profil"), data=data)

    def test_profile_change(self):
        self.client.login(email="gab@gab.com",
                          password="123456789")
        # données qui seront envoyées avec client.post
        data = {
            "email": "gab@gab.com",
            "password": "123456789",
            "first_name": "Patrick",
            "last_name": "Martin"
        }
        # requete post dans ma vue account:profil en passant les data ci-dessus (correspondent aux champs)
        resp = self.client.post(reverse("accounts:profil"), data=data)
        # lorsque ma requete est exécutée j'ai un redirect dans ma vue donc je teste si j'ai bien un statut 302
        self.assertEqual(resp.status_code, 302)
        # récupère l'utilisateur depuis la bdd pour voir s'il est bien modifié
        # on n'utilise pas directement self.user car c'est juste une variable. Cette dernière n'est pas modifiée
        # juste la BDD qui est modifiée
        patrick: Shopper = Shopper.objects.get(email="gab@gab.com")
        self.assertEqual(patrick.last_name, "Martin")
