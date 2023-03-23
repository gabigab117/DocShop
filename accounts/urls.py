from django.urls import path
from accounts.views import signup, logout_user, login_user, profil, set_default_shipping_address

app_name = "accounts"

urlpatterns = [
    path('profil/', profil, name="profil"),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('profil/set-default/<int:pk>/', set_default_shipping_address, name="set-default-shipping"),
]
