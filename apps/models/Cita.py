from django.db import models
from .Paciente import Paciente
from .Odontologo import Odontologo


class Cita(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Atendida', 'Atendida'),
        ('Cancelada', 'Cancelada'),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name='citas',
        verbose_name='Paciente'
    )
    odontologo = models.ForeignKey(
        Odontologo,
        on_delete=models.PROTECT,
        related_name='citas',
        verbose_name='Odontólogo'
    )
    fecha = models.DateField('Fecha de atención')
    hora = models.TimeField('Hora de atención')
    motivo = models.CharField('Motivo de consulta', max_length=200)
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default='Pendiente')
    observaciones = models.TextField('Observaciones', blank=True)

    class Meta:
        db_table = 'citas'
        ordering = ['-fecha', '-hora']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def __str__(self):
        return f"Cita #{self.pk}: {self.paciente.nombres} {self.paciente.apellidos} - {self.fecha} {self.hora.strftime('%H:%M') if hasattr(self.hora, 'strftime') else self.hora}"
