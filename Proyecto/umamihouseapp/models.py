from django.db import models

class TipoPlato(models.TextChoices):
    ENTRANTE = 'ENTRANTE', 'Entrante'
    SUSHI = 'SUSHI', 'Sushi'
    PLATO_PRINCIPAL = 'PLATO_PRINCIPAL', 'Plato_principal'
    POSTRE= 'POSTRE', 'Postre'
    BEBIDA= 'BEBIDA', 'Bebida'

class NumMesa(models.TextChoices):
    MESA1 = 'MESA1', 'Mesa1'
    MESA2 = 'MESA2', 'Mesa2'
    MESA3 = 'MESA3', 'Mesa3'
    MESA4 = 'MESA4', 'Mesa4'
    MESA5 = 'MESA5', 'Mesa5'

class Plato(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    tipo_plato = models.CharField(
        max_length=50,
        choices=TipoPlato.choices,
        default=TipoPlato.ENTRANTE)

#Es un método que podemos modifica para que se muestre el objeto de cierta forma.
    def __str__(self):
        return self.nombre

class Pedido(models.Model):
