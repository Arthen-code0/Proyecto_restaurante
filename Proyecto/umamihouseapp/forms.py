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


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'tipo_plato']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'imagen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL de la imagen'}),
            'tipo_plato': forms.Select(attrs={'class': 'form-control'}),
        }