import datetime
from collections import defaultdict
from gc import get_objects
from sqlite3 import IntegrityError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from pycparser.ply.yacc import Production
from .forms import RegistroForm, LoginForm, PlatoForm, UsuarioForm, PedidoLineaForm
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


# @user_passes_test(es_cocinero)
def cocinero(request):
    return render(request, 'cocinero_pedidos.html')


# @user_passes_test(es_camarero)
def camarero_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha')
    return render(request, 'camarero_pedidos.html', {'pedidos': pedidos})


def pagina_menu(request):
    platos = list(Plato.objects.filter(estado_plato=1))
    ORDEN_TIPO = {
        'ENTRANTE': 1,
        'SUSHI': 2,
        'PLATO_PRINCIPAL': 3,
        'POSTRE': 4,
        'BEBIDA': 5,
    }

    platos_ordenados = sorted(platos, key=lambda p: ORDEN_TIPO.get(p.tipo_plato.strip(), 99))

    return render(request, 'pagina_menu.html', {'platos': platos_ordenados})


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
                return render(request, 'crear_plato.html', {'form': form, 'error': error_msg})
        else:
            print("Errores formulario:", form.errors)
    else:
        form = PlatoForm()
    return render(request, 'crear_plato.html', {'form': form})


def editar_plato(request, plato_id, ):
    plato = get_object_or_404(Plato, pk=plato_id)
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('modificar_menu')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'modificar_plato.html', {'form': form})


def estado_plato(request, plato_id):
    plato = get_object_or_404(Plato, pk=plato_id)
    plato.estado_plato = 0 if plato.estado_plato == 1 else 1
    plato.save()
    return redirect('menu')


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


def alta_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.alta_usuario = 0 if usuario.alta_usuario == 1 else 1
    usuario.save()
    return redirect('ver_usuarios')


def vista_usuarios(request):
    users = User.objects.all()
    return render(request, 'ver_usuarios.html', {'Users': users})


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
                    precio_unitario=item['precio']
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


@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha')

    pedidos_con_totales = []
    for pedido in pedidos:
        total = sum(linea.precio_unitario * linea.cantidad for linea in pedido.pedidolinea_set.all())
        pedidos_con_totales.append({
            'pedido': pedido,
            'total': total
        })

    return render(request, 'mis_pedidos.html', {'pedidos': pedidos_con_totales})


# Vista para añadir un pedido
#@login_required
def agregar_plato_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        form = PedidoLineaForm(request.POST)
        if form.is_valid():
            try:
                linea = form.save(commit=False)
                linea.pedido = pedido

                # Si no se especificó precio, usar el del plato
                if not linea.precio_unitario:
                    linea.precio_unitario = linea.plato.precio

                linea.save()
                messages.add_message(request, messages.SUCCESS, "Plato agregado correctamente")
                return redirect('camarero_pedidos')

            except Exception as e:
                messages.add_message(request, messages.ERROR, f"Error al guardar: {str(e)}")
    else:
        form = PedidoLineaForm()

    return render(request, 'agregar_plato(camarero).html', {
        'form': form,
        'pedido': pedido
    })

#@login_required
def eliminar_plato_pedido(request, pedido_linea_id):
    linea = get_object_or_404(PedidoLinea, id=pedido_linea_id)
    if request.method == 'POST':
        linea.delete()
        return redirect('camarero_pedidos')

    return render(request, 'camarero_pedidos.html', {'linea': linea})

def camarero_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha')
    return render(request, 'camarero_pedidos.html', {'pedidos': pedidos})
