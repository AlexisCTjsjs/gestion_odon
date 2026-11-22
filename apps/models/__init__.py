"""Modelos del Consultorio Odontológico Sonrisa Perfecta."""

from .Paciente import Paciente
from .Especialidad import Especialidad
from .Odontologo import Odontologo
from .Cita import Cita
from .Diagnostico import Diagnostico
from .Tratamiento import Tratamiento
from .Receta import Receta

__all__ = [
    'Paciente',
    'Especialidad',
    'Odontologo',
    'Cita',
    'Diagnostico',
    'Tratamiento',
    'Receta',
]
