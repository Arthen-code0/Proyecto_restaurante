from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from oracledb import defaults



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
        default=TipoPlato.ENTRANTE,
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)  # Cambiado de auto_now_add
    fecha_modificacion = models.DateTimeField(auto_now=True)

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
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'rol']


    def __str__(self):
        return f"{self.email} - {self.nombreUsuario} ({self.rol})"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=False)
    mail = models.EmailField(max_length=150)
    imagen_url = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + " " + self.nombre + "," + self.apellido


class Empleado(models.Model):
    nombreCompleto = models.CharField(max_length=500)
    fecha_nacimiento = models.DateField(null=False)
    mail = models.EmailField(max_length=150)
    imagen_url = models.CharField(max_length=1000)
    user = models.OneToOneField(User, null=True, on_delete=models.DO_NOTHING)
    rol = models.CharField(max_length=50, choices=Rol.choices, default=Rol.COCINERO)
    fecha_creacion = models.DateTimeField(default=timezone.now)  # Cambiado de auto_now_add
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + " " + self.nombreCompleto


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
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.codigo) + " " + str(self.fecha) + " " + str(self.cliente.nombreUsuario)


class PedidoLinea(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio_compra = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.plato.nombre) + " " + str(self.cantidad) + " " + str(self.precio_compra)

