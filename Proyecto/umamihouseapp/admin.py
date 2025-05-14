from django.contrib import admin

from umamihouseapp.models import Plato, User, Cliente, Pedido, Empleado, PedidoLinea

# Register your models here.
admin.site.register(Plato)
admin.site.register(User)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Pedido)
admin.site.register(PedidoLinea)