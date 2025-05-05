from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .form import RegistroForm, LoginForm
from .models import User

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
