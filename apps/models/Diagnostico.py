from django.db import models
from .Cita import Cita


class Diagnostico(models.Model):
    cita = models.ForeignKey(
        Cita,
        on_delete=models.PROTECT,
        related_name='diagnosticos',
        verbose_name='Cita'
    )
    descripcion = models.TextField('Diagnóstico clínico')
    recomendaciones = models.TextField('Recomendaciones', blank=True)
    fecha = models.DateField('Fecha del diagnóstico')

    class Meta:
        db_table = 'diagnosticos'
        ordering = ['-fecha', '-id']
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'

    def __str__(self):
        return f"Diagnóstico #{self.pk} - Cita #{self.cita_id} ({self.cita.paciente.nombres} {self.cita.paciente.apellidos})"
