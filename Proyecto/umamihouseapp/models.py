from django.db import models

class TipoPlato(models.TextChoices):
    ENTRANTE = 'ENTRANTE', 'Entrante'
    SUSHI = 'SUSHI', 'Sushi'
    PLATO_PRINCIPAL = 'PLATO_PRINCIPAL', 'Plato_principal'
    POSTRE= 'POSTRE', 'Postre'
    BEBIDA= 'BEBIDA', 'Bebida'

class Plato(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField()
    tipo_plato = models.CharField(
        max_length=50,
        choices=TipoPlato.choices,
        default=TipoPlato.ENTRANTE)
