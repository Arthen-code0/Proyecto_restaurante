from django.contrib.auth import views
from django.urls import path
from umamihouseapp.views import *

urlpatterns = [
    # URL, METODO, NOMBRE_ABREVIADO
    path('home', pagina_principal, name='home'),
    path('', pagina_principal, name='home'),
    path('menu/', pagina_menu, name='menu'),
    path('registro/', registrar_usuario, name='registrar_usuario'),
    path('inicio_sesion/', login_usuario, name='login_usuario'),
    path('crear_plato/', crear_plato, name='crear_plato'),
    path('formulario_pago/', formulario_pago, name='formulario_pago'),
    path('tu_pedido/', tu_pedido, name='tu_pedido'),
    path('modificar_menu/', modificar_menu, name='modificar_menu'),
    path('mesas/', mesas, name='mesas'),
    path('cocinero/', cocinero, name='cocinero'),
    path('camarero/', camarero, name='camarero'),

    # redireccion una vez que el usuario se ha deslogueado
    path('logout/', cerrar_sesion, name='logout'),
    path('pagina_usuario/', Pagina_usuario, name='pagina_usuario'),
]
