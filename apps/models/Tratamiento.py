from django.db import models
from .Diagnostico import Diagnostico


class Tratamiento(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Finalizado', 'Finalizado'),
    ]

    diagnostico = models.ForeignKey(
        Diagnostico,
        on_delete=models.PROTECT,
        related_name='tratamientos',
        verbose_name='Diagnóstico'
    )
    nombre = models.CharField('Nombre del tratamiento', max_length=150)
    descripcion = models.TextField('Descripción del procedimiento', blank=True)
    fecha_inicio = models.DateField('Fecha de inicio')
    fecha_fin = models.DateField('Fecha de finalización', null=True, blank=True)
    costo = models.DecimalField('Costo del tratamiento', max_digits=10, decimal_places=2)
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default='Pendiente')

    class Meta:
        db_table = 'tratamientos'
        ordering = ['-fecha_inicio', '-id']
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'

    def __str__(self):
        return f"{self.nombre} (S/ {self.costo}) - {self.estado}"

