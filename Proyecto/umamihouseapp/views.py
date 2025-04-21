from django.shortcuts import render

def pagina_principal(request):
    return render(request, 'pagina_principal.html')

def pagina_menu(request):
    return render(request, 'pagina_menu.html')

def registrar_usuario(request):
    return render(request, 'registrarse.html')
