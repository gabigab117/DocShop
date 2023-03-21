from django import forms
from store.models import Order


class OrderForm(forms.ModelForm):
    # je modifie le widget utilisé
    quantity = forms.CharField(choices=[(i, i) for i in range(1, 11)])

    class Meta:
        model = Order
        # uniquement le champ de la quantité
        fields = ["quantity"]
