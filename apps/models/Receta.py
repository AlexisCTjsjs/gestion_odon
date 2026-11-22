from django.db import models
from .Diagnostico import Diagnostico


class Receta(models.Model):
    diagnostico = models.ForeignKey(
        Diagnostico,
        on_delete=models.PROTECT,
        related_name='recetas',
        verbose_name='Diagnóstico'
    )
    medicamento = models.CharField('Medicamento indicado', max_length=150)
    dosis = models.CharField('Dosis prescrita', max_length=100)
    frecuencia = models.CharField('Frecuencia de administración', max_length=100)
    duracion = models.CharField('Duración del tratamiento', max_length=100)
    indicaciones = models.TextField('Indicaciones adicionales', blank=True)
    fecha_emision = models.DateField('Fecha de emisión')

    class Meta:
        db_table = 'recetas'
        ordering = ['-fecha_emision', '-id']
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'

    def __str__(self):
        return f"Receta #{self.pk} - {self.medicamento} ({self.dosis})"
