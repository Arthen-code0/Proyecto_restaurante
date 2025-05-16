import datetime
from collections import defaultdict
from gc import get_objects
from sqlite3 import IntegrityError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from pycparser.ply.yacc import Production
from .forms import RegistroForm, LoginForm, PlatoForm, UsuarioForm
from .models import User, Plato, Mesa
from .forms import RegistroForm, LoginForm, PlatoForm
from .models import User, Plato, Pedido, PedidoLinea

import json
from django.http import JsonResponse
from django.utils import timezone
import random
import string


# Para el usuario administrador
def es_admin(user):
    if not user.is_authenticated or not user.rol == 'ADMIN':
        raise PermissionDenied
    return True


# Para el usuario camarero
def es_camarero(user):
    if not user.is_authenticated or not user.rol == 'CAMARERO':
        raise PermissionDenied
    return True


# Para el usuario cocinero
def es_cocinero(user):
    if not user.is_authenticated or not user.rol == 'COCINERO':
        raise PermissionDenied
    return True


def pagina_principal(request):
    return render(request, 'pagina_principal.html')


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'cliente'
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            usuario = authenticate(request, email=email, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'inicio_sesion.html', {'form': form})


# Deslogueo del usuario
def cerrar_sesion(request):
    logout(request)
    return redirect('home')


# @user_passes_test(es_admin)
def crear_plato(request):
    return render(request, 'crear_plato.html')


# @user_passes_test(es_admin)
def modificar_menu(request):
    platos = Plato.objects.all()
    return render(request, 'modificar_menu.html', {'platos': platos})

@login_required
def formulario_pago(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    return render(request, 'formulario_pago.html', {'pedido': pedido})

@login_required
def tu_pedido(request):
    return render(request, 'tu_pedido.html')


def mesas(request):
    return render(request, 'mesas.html')


@user_passes_test(es_cocinero)
def cocinero(request):
    return render(request, 'cocinero.html')


@user_passes_test(es_camarero)
def camarero(request):
    return render(request, 'camarero.html')


def pagina_menu(request):
    platos = Plato.objects.all()
    return render(request, 'pagina_menu.html', {'platos': platos})


# Modificar, Eliminar y Agregar para la carta desde la vista de un administrador

def crear_plato(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data.pop('id', None)
        form = PlatoForm(data)
        if form.is_valid():
            try:
                form.save()
                return redirect('menu')
            except IntegrityError as e:
                error_msg = str(e)
                print("Error guardando plato:", error_msg)
                return render(request, 'Crea_p.html', {'form': form, 'error': error_msg})
        else:
            print("Errores formulario:", form.errors)
    else:
        form = PlatoForm()
    return render(request, 'Crea_p.html', {'form': form})


def editar_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'crear_plato.html', {'form': form})


def eliminar_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.delete()
        return redirect('pagina_menu')
    return render(request, 'eliminar_producto', {'plato': plato})


def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('ver_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form})


def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    return redirect('ver_usuarios')


def vista_usuarios(request):
    users = User.objects.all()
    return render (request, 'Ver_usuarios.html', {'Users': users})

def mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'mesas.html', {'mesas': mesas})

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        try:
            carrito = json.loads(request.POST.get('carrito', '[]'))

            if not carrito:
                return JsonResponse({'success': False, 'error': 'Carrito vacío'})

            # Generar código aleatorio
            codigo = 'PED-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            # Crear pedido
            pedido = Pedido.objects.create(
                codigo=codigo,
                fecha=timezone.now(),
                cliente=request.user
            )

            # Crear líneas de pedido
            for item in carrito:
                plato = Plato.objects.get(id=item['id'])
                PedidoLinea.objects.create(
                    pedido=pedido,
                    plato=plato,
                    cantidad=item['cantidad'],
                    precio_compra=item['precio']
                )

            # Redirigir al formulario de pago
            return redirect('formulario_pago', pedido_id=pedido.id)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def cambiar_estado(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    if request.method == 'POST':
        estado_new = request.POST.get('estado')
        if estado_new in dict(Mesa._meta.get_field('EstadoMesa').choices):
            mesa.EstadoMesa = estado_new
            mesa.save()
    return redirect('mesas')


#def add_carrito(request, id):
#    carrito = request.session.get('carrito', 0)
#    carrito = request.session.get(str(id), 0)
#
#    if producto_en_carrito == 0:
#        #NO
#        carrito[str(id)] = 1
#    else:
#        carrito[str(id)] += 1
#
#    request.session['carrito'] = carrito
#    return redirect('tienda')


# def ver_carrito(request):
#    carrito = {}
#    carrito_session = request.session.get('carrito', {})

#    for k, v in carrito.session.items():
#        producto = Producto.objects.get(id=k)
#        carrito[producto] = v
#        total += prodcuto.precio * v
#
# return render(request, 'carrito.html', {'carrito', })

# def compra(request):
#    nuevo_pedido = Pedido()
#    nuevo_pedido.codigo = 'CP0001' #Codigo aleatorio (hablar con jose para la creacion de un trigger)
#    nuevo_pedido.fecha = datetime.now()
#    nuevo_pedido.cliente = request.user

#    for k, v in carrito_session.items():
#        linea_pedido = LineaPedido()

#        producto = Producto.objects.get(id=k)
#        linea_pedido.producto = producto
#        linea_pedido.precio = producto.precio
#        linea_pedido.cantidad = v
#        linea_pedido.pedido = nuevo_pedido
#        linea_pedido.save()

#    linea_pedido.save()
