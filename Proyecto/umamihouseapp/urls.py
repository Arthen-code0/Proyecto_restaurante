from django.urls import path
from umamihouseapp.views import *

urlpatterns = [
    path('home', pagina_principal, name='home'),
    path('', pagina_principal, name='home'),
    path('menu/', pagina_menu, name='menu'),
    path('registro/', registrar_usuario, name='registrar_usuario'),
    path('inicio_sesion/', login_usuario, name='login_usuario'),
    path('crear_plato/', crear_plato, name='crear_plato'),
    path('formulario_pago/', formulario_pago, name='formulario_pago'),
    path('tu_pedido/', tu_pedido, name='tu_pedido'),
    path('navbarmobiles/', navbarmobiles, name='navbarmobiles'),
    path('mesas/', mesas, name='mesas'),
]
