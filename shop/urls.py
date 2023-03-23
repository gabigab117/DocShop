from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from store.views import index

from shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('account/', include('accounts.urls')),
    path('store/', include('store.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
