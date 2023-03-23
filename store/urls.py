from django.urls import path
from store.views import product_detail, add_to_cart, cart, delete_cart, create_checkout_session, checkout_success, stripe_webhook, update_quantities


app_name = "store"

urlpatterns = [

    path('stripe-webhook/', stripe_webhook, name="stripe-webhook"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('cart/', cart, name="cart"),
    path('cart/update_quantities/', update_quantities, name="update-quantities"),
    path('cart/success/', checkout_success, name="checkout-success"),
    path('cart/create-checkout-session', create_checkout_session, name="create-checkout-session"),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add-to-cart/', add_to_cart, name="add-to-cart")
]
