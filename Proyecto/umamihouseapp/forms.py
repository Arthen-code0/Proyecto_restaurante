from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *


class RegistroForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    email = forms.EmailField(label="Correo")
    password = forms.CharField(widget=forms.PasswordInput())
    telefono = forms.CharField(max_length=100)
    fecha_nacimiento = forms.DateField()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'nombre', 'password', 'apellido', 'telefono', 'fecha_nacimiento']


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Correo")


# Formulario para Eliminar,Modificar y Aregar PLATO
class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = '__all__'

#Formulario de usuario para modicarlos

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'rol']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de nacimiento', 'type': 'date'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }
class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['EstadoMesa']
        widgets = {
            'EstadoMesa': forms.RadioSelect(choices=EstadoMesa.choices),
        }
