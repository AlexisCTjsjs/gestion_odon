from django.db import models


class Paciente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField('Documento de identidad', max_length=8, unique=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento')
    telefono = models.CharField('Número telefónico', max_length=20)
    direccion = models.CharField('Dirección', max_length=200)
    correo = models.EmailField('Correo electrónico')
    created_at = models.DateTimeField('Fecha de registro automática', auto_now_add=True)

    class Meta:
        db_table = 'pacientes'
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} (DNI: {self.dni})"

