from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect

from umamihouseapp.form import RegistroForm, LoginForm


def pagina_principal(request):
    return render(request, 'pagina_principal.html')


def pagina_menu(request):
    return render(request, 'pagina_menu.html')


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit==False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('login')
        else:
            form = RegistroForm()
            return render(request, 'registro.html', {'form': form})


def inicio_de_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            usuario = authenticate(request, email=email, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('login')
            else:
                form = LoginForm()
                return render(request, 'registro.html', {'form': form})

#HAY QUE HACER EL BOTON DE CERRAR SESION EN LOGIN 
def logout_usuario(request):
    logout(request)
    return redirect('login')

def crear_plato(request):
    return render(request, 'crear_plato.html')


def formulario_pago(request):
    return render(request, 'formulario_pago.html')


def tu_pedido(request):
    return render(request, 'tu_pedido.html')


def camarero(request):
    return render(request, 'camarero.html')


def cocinero(request):
    return render(request, 'cocinero.html')


def mesas(request):
    return render(request, 'mesas.html')
