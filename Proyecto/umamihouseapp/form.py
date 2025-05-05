from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class RegistroForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    email = forms.EmailField(label="Correo")
    password = forms.CharField(widget=forms.PasswordInput())
    rol = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['email', 'nombre', 'rol', 'password', 'apellido']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Correo")