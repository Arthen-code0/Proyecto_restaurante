from django.contrib.auth import views
from django.urls import path, include
from umamihouseapp.views import *

urlpatterns = [
    # URL, METODO, NOMBRE_ABREVIADO
    path('home', pagina_principal, name='home'),
    path('', pagina_principal, name='home'),
    path('menu/', pagina_menu, name='menu'),
    path('registro/', registrar_usuario, name='registrar_usuario'),
    path('inicio_sesion/', login_usuario, name='login_usuario'),
    path('crear_plato/', crear_plato, name='crear_plato'),
    path('formulario-pago/<int:pedido_id>/', formulario_pago, name='formulario_pago'),
    path('mesas/', mesas, name='mesas'),
    path('cocinero/', cocinero, name='cocinero'),
    path('logout/', cerrar_sesion, name='logout'),
    path('crear-pedido/', crear_pedido, name='crear_pedido'),

    # PRODUCTOS Modificar, Eliminar y Agregar
    path('modificar_menu/', modificar_menu, name='modificar_menu'),
    path('agregar_plato/', crear_plato, name='crear_plato'),
    path('editar_plato/<int:plato_id>/', editar_plato, name='editar_plato'),
    path('eliminar_plato/<int:plato_id>/', estado_plato, name='eliminar_plato'),

    # Usuarios, modificar y eliminar
    path('ver_usuarios/', vista_usuarios, name='ver_usuarios'),
    path('editar_usuario/<int:user_id>/', editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', alta_usuario, name='eliminar_usuario'),
    path('mesas/', mesas, name='mesas'),
    path('mesas/<int:mesa_id>/cambiar/', cambiar_estado, name='cambiar_estado'),
    path('mis_pedidos/', mis_pedidos, name='mis_pedidos'),
    path('camarero_pedidos/', camarero_pedidos, name='camarero_pedidos'),
    path('eliminar_plato_pedido/<int:pedido_linea_id>/', eliminar_plato_pedido, name='eliminar_plato_pedido'),
    path('agregar_plato_pedido/<int:pedido_id>/', agregar_plato_pedido, name='agregar_plato_pedido'),
    path('cocinero/cambiar-estado/<int:pedido_id>/', cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('crear_reserva/', crear_reserva, name='hacer_reserva'),
    path('editar_reserva/<int:reserva_id>/', editar_reserva, name='editar_reserva'),
    path('ver_reserva/', ver_reserva, name='ver_reserva'),

]
