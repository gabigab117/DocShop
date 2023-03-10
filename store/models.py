from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from shop.settings import AUTH_USER_MODEL

'''
Product
- Nom
- Prix
- Stock
- Description
- Image
'''

class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.stock})"

    def get_absolute_url(self):
        # nom url + slug (on le retrouve dans url <str:slug>)
        return reverse("product", kwargs={"slug": self.slug})

# article (order)
'''
utilisateur,
produit,
quantité
commandé ou non
'''
class Order(models.Model):
    # user peut avoir plusieurs order
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # un seul product par order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

# panier utilisateur (cart)
'''
utilisateur,
Articles
commandé ou non
date commande
'''

class Cart(models.Model):
    # one to one car l'utilisateur ne peut avoir qu'un seul panier. Si j'utilise Foreign als unique=True
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # plusieurs articles peuvent être ajoutés donc ManytoMany
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        # je détache les articles de mon panier avec clear
        self.orders.clear()
        
        super().delete(*args, **kwargs)
