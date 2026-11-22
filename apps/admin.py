from django.contrib import admin
from .models import Paciente, Especialidad, Odontologo, Cita, Diagnostico, Tratamiento, Receta

for modelo in (Paciente, Especialidad, Odontologo, Cita, Diagnostico, Tratamiento, Receta):
    admin.site.register(modelo)

admin.site.site_header = 'Sonrisa Perfecta - Administración'
admin.site.site_title = 'Sonrisa Perfecta'
admin.site.index_title = 'Panel de Administración Odontológica'
