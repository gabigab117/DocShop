from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from store.views import index, product_detail, add_to_cart, cart, delete_cart, create_checkout_session, checkout_success, stripe_webhook
from accounts.views import signup, logout_user, login_user, profil, set_default_shipping_address
from shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('profil/', profil, name="profil"),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('profil/set-default/<int:pk>/', set_default_shipping_address, name="set-default-shipping"),
    path('stripe-webhook/', stripe_webhook, name="stripe-webhook"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('cart/', cart, name="cart"),
    path('cart/success/', checkout_success, name="checkout-success"),
    path('cart/create-checkout-session', create_checkout_session, name="create-checkout-session"),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add-to-cart/', add_to_cart, name="add-to-cart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
