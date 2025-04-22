from django.shortcuts import render


def pagina_principal(request):
    return render(request, 'pagina_principal.html')


def pagina_menu(request):
    return render(request, 'pagina_menu.html')


def registrar_usuario(request):
    return render(request, 'registro.html')


def inicio_de_sesion(request):
    return render(request, 'inicio_sesion.html')

def crear_plato(request):
    return render(request, 'crear_plato.html')