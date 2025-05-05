import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from pycparser.ply.yacc import Production

from .form import RegistroForm, LoginForm
from .models import User, Pedido


def pagina_principal(request):
    return render(request, 'pagina_principal.html')

def pagina_menu(request):
    return render(request, 'pagina_menu.html')

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('login')
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
                return redirect('inicio')
    else:
        form = LoginForm()
    return render(request, 'inicio_sesion.html', {'form': form})

def crear_plato(request):
    return render(request, 'crear_plato.html')

def formulario_pago(request):
    return render(request, 'formulario_pago.html')

def tu_pedido(request):
    return render(request, 'tu_pedido.html')

def navbarmobiles(request):
    return render(request, 'navbarmoviles.html')

def mesas(request):
    return render(request, 'mesas.html')

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


#def ver_carrito(request):
#    carrito = {}
#    carrito_session = request.session.get('carrito', {})

#    for k, v in carrito.session.items():
#        producto = Producto.objects.get(id=k)
#        carrito[producto] = v
#        total += prodcuto.precio * v
#
# return render(request, 'carrito.html', {'carrito', })

#def compra(request):
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