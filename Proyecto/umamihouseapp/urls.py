from django.urls import path
from umamihouseapp.views import pagina_principal, pagina_menu

urlpatterns = [
    path('home', pagina_principal, name='home'),
    path('', pagina_principal, name='home'),
    path('menu/', pagina_menu, name='menu'),
]
