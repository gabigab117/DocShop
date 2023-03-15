from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


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
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Shopper(AbstractUser):
    # écraser le champ username pour dire que l'on en a pas besoin
    username = None
    email = models.EmailField(unique=True, max_length=240)

    # champ utilisé pour se connecter : (il est automatiquement considéré comme requis)
    USERNAME_FIELD = "email"
    # champs obligatoires pour la création d'un compte / je laisse vide pour le moment
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
