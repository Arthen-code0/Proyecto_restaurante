from django.urls import path
from umamihouseapp.views import pagina_principal, pagina_menu, registrar_usuario, inicio_de_sesion, crear_plato

urlpatterns = [
    path('home', pagina_principal, name='home'),
    path('', pagina_principal, name='home'),
    path('menu/', pagina_menu, name='menu'),
    path('registro/', registrar_usuario, name='registrar_usuario'),
    path('inicio_de_sesion/', inicio_de_sesion, name='inicio_de_sesion'),
    path('crear_plato/', crear_plato, name='crear_plato'),
]
