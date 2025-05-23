from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _



class TipoPlato(models.TextChoices):
    ENTRANTE = 'ENTRANTE', 'Entrante'
    SUSHI = 'SUSHI', 'Sushi'
    PLATO_PRINCIPAL = 'PLATO_PRINCIPAL', 'Plato_principal'
    POSTRE = 'POSTRE', 'Postre'
    BEBIDA = 'BEBIDA', 'Bebida'


class EstadoMesa(models.TextChoices):
    RESERVADA = 'RESERVADA', 'Reservada'
    OCUPADA = 'OCUPADA', 'Ocupada'
    DISPONIBLE = 'DISPONIBLE', 'Disponible'


class Rol(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrador'
    COCINERO = 'COCINERO', 'Cocinero'
    CAMARERO = 'CAMARERO', 'Camarero'
    CLIENTE = 'CLIENTE', 'Cliente'


class Mesa(models.Model):
    EstadoMesa = models.CharField(max_length=50, choices=EstadoMesa.choices, default=EstadoMesa.DISPONIBLE)


class Plato(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    imagen = models.CharField(max_length=2000)
    tipo_plato = models.CharField(
        max_length=50,
        choices=TipoPlato.choices,
        default=TipoPlato.PLATO_PRINCIPAL,
    )
    estado_plato = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre



class UserManager(BaseUserManager):
    def create_user(self, email, nombreUsuario, rol, password=None):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nombreUsuario=nombreUsuario,
            rol=rol
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombreUsuario, password=None, **extra_fields):
        extra_fields.setdefault('rol', Rol.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(
            email=email,
            nombreUsuario=nombreUsuario,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    nombre = models.CharField(_('nombre'), max_length=100, blank=True)
    apellido = models.CharField(_('apellido'), max_length=100, blank=True)
    telefono = models.CharField(_('telefono'), max_length=100, blank=True)
    fecha_nacimiento = models.DateField(_('fecha_nacimiento'), null=True)
    rol = models.CharField(
        max_length=10,
        choices=Rol.choices,
        default=Rol.CLIENTE,
    )
    alta_usuario = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'rol']


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class Pedido(models.Model):
    PREPARANDO = 1
    EN_PROCESO = 2
    FINALIZADO = 3

    ESTADO_CHOICES = [
        (PREPARANDO, 'Preparando'),
        (EN_PROCESO, 'En proceso'),
        (FINALIZADO, 'Finalizado'),
    ]

    codigo = models.CharField(max_length=100, blank=True, null=False)
    fecha = models.DateTimeField()
    cliente = models.ForeignKey('User', on_delete=models.DO_NOTHING, related_name='pedidos')
    estado = models.IntegerField(
        choices=ESTADO_CHOICES,
        default=PREPARANDO
    )


    def __str__(self):
        return str(self.codigo) + " " + str(self.fecha) + " " + str(self.cliente.nombreUsuario)


class PedidoLinea(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField(default=1)  # Añadido valor por defecto
    precio_unitario = models.DecimalField(max_digits=5, decimal_places=2)
    precio_total = models.DecimalField(max_digits=5, decimal_places=2, editable=False, default=0.00)

    def save(self, *args, **kwargs):
        # Asegurar que el precio_unitario tenga valor
        if not self.precio_unitario and hasattr(self.plato, 'precio'):
            self.precio_unitario = self.plato.precio

        # Validar valores antes del cálculo
        if self.cantidad is None or self.precio_unitario is None:
            raise ValueError("Tanto cantidad como precio_unitario deben tener valores válidos")

        # Calcular el total
        self.precio_total = self.cantidad * self.precio_unitario

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plato.nombre} x{self.cantidad} = {self.precio_total}€"

