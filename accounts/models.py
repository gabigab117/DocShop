from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from iso3166 import countries


class CustomUserManager(BaseUserManager):
    # kwargs si prénom nom de famille etc...
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Vous devez renseigner un email")

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        kwargs['is_active'] = True

        return self.create_user(email=email, password=password, **kwargs)


class Shopper(AbstractUser):
    # écraser le champ username pour dire que l'on en a pas besoin
    username = None
    email = models.EmailField(unique=True, max_length=240)

    # champ utilisé pour se connecter : (il est automatiquement considéré comme requis)
    USERNAME_FIELD = "email"
    # champs obligatoires pour la création d'un compte / je laisse vide pour le moment
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class ShippingAddress(models.Model):
    # comme je peux avoir plusieurs adresses pour un user pas de one mais une foreign
    user = models.ForeignKey(Shopper, on_delete=models.CASCADE)
    name = models.CharField(max_length=240)
    address_1 = models.CharField(max_length=1024, help_text="Adresse de voirie et numéro de rue")
    address_2 = models.CharField(max_length=1024, help_text="Bâtiment, étage, lieu-dit...", blank=True)
    city = models.CharField(max_length=1024)
    zip_code = models.CharField(max_length=32)
    # liste de tuple avec en 1er deux lettres (bd) et après le pays
    country = models.CharField(max_length=2, choices=[(c.alpha2.lower(), c.name) for c in countries])

    def __str__(self):
        return f"{self.user}, {self.name}"
