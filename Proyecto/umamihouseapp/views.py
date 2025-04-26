from django.shortcuts import render


def pagina_principal(request):
    return render(request, 'pagina_principal.html')


def pagina_menu(request):
    return render(request, 'pagina_menu.html')


def registrar_usuario(request):
    return render(request, 'registrarse.html')


def inicio_de_sesion(request):
    return render(request, 'inicio_de_sesion.html')


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
