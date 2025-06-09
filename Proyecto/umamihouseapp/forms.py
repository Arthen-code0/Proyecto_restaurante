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


# Formulario para Eliminar, Modificar y Agregar PLATO
class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'tipo_plato']


# Formulario de usuario para modificarlos
class UsuarioForm(forms.ModelForm):
    class Meta:
        # Tabla en la que guardar los datos
        model = User
        # Campos que se deben mostrar en el formulario
        fields = ['nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'rol']
        # Tipo de datos en los respectivos campos
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'fecha_nacimiento': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Fecha de nacimiento', 'type': 'date'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }
class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['EstadoMesa']
        widgets = {
            'EstadoMesa': forms.RadioSelect(choices=EstadoMesa.choices),
        }

class PedidoLineaForm(forms.ModelForm):
    class Meta:
        model = PedidoLinea
        fields = ['plato', 'cantidad']


class ReservaMesaUsuarioForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_reserva', 'hora_reserva', 'numero_personas']
        widgets = {
            'fecha_reserva': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de la reserva', 'type': 'date'}),
            'hora_reserva': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Hora de la reserva', 'type': 'time'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Numero de personas', 'type': 'number', 'min': 1, 'max': 20}),
        }


class ResenaUsuarioForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['comentario', 'puntuacion']
        widgets = {
            'comentario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comentario de la reseña', 'type': 'text'}),
            'puntuacion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Puntuacion de la reseña', 'type': 'number', 'min': 1, 'max': 5}),
        }
