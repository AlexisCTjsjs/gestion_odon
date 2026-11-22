from django.db import models
from .Especialidad import Especialidad


class Odontologo(models.Model):
    ESTADOS = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    nombres = models.CharField('Nombres', max_length=100)
    apellidos = models.CharField('Apellidos', max_length=100)
    numero_colegiatura = models.CharField('Número de colegiatura', max_length=30)
    telefono = models.CharField('Teléfono', max_length=20)
    correo = models.EmailField('Correo electrónico')
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name='odontologos',
        verbose_name='Especialidad'
    )
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default='Activo')

    class Meta:
        db_table = 'odontologos'
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Odontólogo'
        verbose_name_plural = 'Odontólogos'

    def __str__(self):
        return f"Dr(a). {self.nombres} {self.apellidos}"

