from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Los Models.TextChoices son una especie de ENUM que nos servirán para relacionar con métodos
class TipoPlato(models.TextChoices):
    ENTRANTE = 'ENTRANTE', 'Entrante'
    SUSHI = 'SUSHI', 'Sushi'
    PLATO_PRINCIPAL = 'PLATO_PRINCIPAL', 'Plato_principal'
    POSTRE = 'POSTRE', 'Postre'
    BEBIDA = 'BEBIDA', 'Bebida'


# NumMesa aun no tiene función porque tengo que pensar como hacer el modelo para que los camareros asignen mesas y hagan pedidos,
# perdo supongo que nos serivirá pronto
class NumMesa(models.TextChoices):
    MESA1 = 'MESA1', 'Mesa1'
    MESA2 = 'MESA2', 'Mesa2'
    MESA3 = 'MESA3', 'Mesa3'
    MESA4 = 'MESA4', 'Mesa4'
    MESA5 = 'MESA5', 'Mesa5'


# Rol es para definir el rol del usuario a crear
class Rol(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrador'
    COCINERO = 'COCINERO', 'Cocinero'
    CAMARERO = 'CAMARERO', 'Camarero'
    CLIENTE = 'CLIENTE', 'Cliente'


# Modelo para la creación de platos, se relaciona con el modelo TipoPlato.
class Plato(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    imagen = models.CharField(max_length=2000)
    tipo_plato = models.CharField(
        max_length=50,
        choices=TipoPlato.choices,
        default=TipoPlato.ENTRANTE)

    # el return nos muestra lo que le pasemos de nuestro método (creo que no hacía falta explicar)
    def __str__(self):
        return self.nombre


# Esta clase es un controlador para crear usuarios y superusuarios
class UserManager(BaseUserManager):
    def create_user(self, email, nombre, rol, password=None):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, rol=rol)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, rol='admin', password=None):
        user = self.create_user(email, nombre, rol, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Esta clase crea usuarios
class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('cocinero', 'Cocinero'),
        ('camarero', 'Camarero'),
    )
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=50, choices=Rol.choices, default=Rol.CLIENTE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'rol']

    def __str__(self):
        return self.email + "-" + self.nombreUsuario + ":" + self.rol


# Esta clase crea clientes
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=False)
    mail = models.EmailField(max_length=150)
    imagen_url = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        return str(self.id) + " " + self.nombre + "," + self.apellido


# Esta clase crea cocineros
class Cocinero(models.Model):
    nombreCompleto = models.CharField(max_length=500)
    fecha_nacimiento = models.DateField(null=False)
    # dni = models.CharField(max_length=9)
    mail = models.EmailField(max_length=150)
    imagen_url = models.CharField(max_length=1000)
    user = models.OneToOneField(User, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id) + " " + self.nombreCompleto


# Esta clase crea camareros
class Camarero(models.Model):
    nombreCompleto = models.CharField(max_length=500)
    fecha_nacimiento = models.DateField(null=False)
    # dni = models.CharField(max_length=9)
    mail = models.EmailField(max_length=150)
    imagen_url = models.CharField(max_length=1000)
    user = models.OneToOneField(User, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id) + " " + self.nombreCompleto


# Esta clase crea la lineas de los pedidos online, es decir, una linea que contenga el plato que has pedido, con la cantidad y el precio.
class pedidoLinea(models.Model):
    # on_delete=models.DO_NOTHING nos dice que si el plato del que depende el pedido es eliminado, entonces no haga nada.
    plato = models.ForeignKey(Plato, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio_compra = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.plato.nombre) + " " + str(self.cantidad) + " " + str(self.precio_compra)


# Esta clase crea el pedido completo partiendo de las lineas anteriores
class Pedido(models.Model):
    codigo = models.CharField(max_length=100, blank=True, null=False)
    fecha = models.DateField(null=False)
    cliente = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Pedido_linea = models.ManyToManyField(pedidoLinea)

    def __str__(self):
        return str(self.codigo) + " " + str(self.fecha) + " " + str(self.cliente.nombreUsuario)
