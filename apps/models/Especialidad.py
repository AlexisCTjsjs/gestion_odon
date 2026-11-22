from django.db import models


class Especialidad(models.Model):
    ESTADOS = [
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
    ]

    nombre = models.CharField('Nombre de especialidad', max_length=100)
    descripcion = models.TextField('Descripción', blank=True)
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default='Activa')

    class Meta:
        db_table = 'especialidades'
        ordering = ['nombre']
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'

    def __str__(self):
        return self.nombre

