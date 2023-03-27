from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
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
    slug = models.SlugField(max_length=128, blank=True)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)
    stripe_id = models.CharField(max_length=90, blank=True)

    def __str__(self):
        return f"{self.name} ({self.stock})"

    def save(self, *args, **kwargs):
        '''
       Je peux faire self.slug = self.slug or slugify(self.name)
       en gros si il y a un slug c'est bon sinon on slugify
        '''
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else static("1.jpg")

    def get_absolute_url(self):
        # nom url + slug (on le retrouve dans url <str:slug>)
        return reverse("store:product", kwargs={"slug": self.slug})

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
        return self.user.email

    def order_ok(self):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
            self.orders.clear()
            self.delete()

    def delete(self, *args, **kwargs):
        orders = self.orders.all()

        for order in orders:
            order.delete()
        super().delete(*args, **kwargs)
