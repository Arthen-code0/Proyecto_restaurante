from django.contrib.auth import views
from django.urls import path, include
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
    path('mesas/', mesas, name='mesas'),
    path('cocinero/', cocinero, name='cocinero'),
    path('camarero/', camarero, name='camarero'),

    # redireccion una vez que el usuario se ha deslogueado
    path('logout/', cerrar_sesion, name='logout'),

    # PRODUCTOS Modificar, Eliminar y Agregar
    path('modificar_menu/', modificar_menu, name='modificar_menu'),
    path('agregar_plato/', crear_plato, name='crear_plato'),
    path('agregar_plato/<int:user_id>/', editar_plato, name='editar_plato'),
    path('eliminar_plato/<int:user_id>/', eliminar_plato, name='eliminar_plato'),
]
