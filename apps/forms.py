from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import Paciente, Especialidad, Odontologo, Cita, Diagnostico, Tratamiento, Receta


class FormularioBase(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if isinstance(campo.widget, forms.DateInput):
                campo.widget.input_type = 'date'
            if isinstance(campo.widget, forms.TimeInput):
                campo.widget.input_type = 'time'
            campo.widget.attrs.setdefault('class', 'campo')


class PacienteForm(FormularioBase):
    class Meta:
        model = Paciente
        fields = ['nombres', 'apellidos', 'dni', 'fecha_nacimiento', 'telefono', 'direccion', 'correo']
        widgets = {
            'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d'),
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni', '').strip()
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError('El DNI debe tener exactamente 8 dígitos numéricos.')
        paciente_existente = Paciente.objects.filter(dni=dni)
        if self.instance and self.instance.pk:
            paciente_existente = paciente_existente.exclude(pk=self.instance.pk)
        if paciente_existente.exists():
            raise forms.ValidationError('Ya existe un paciente registrado con este DNI.')
        return dni


class EspecialidadForm(FormularioBase):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class OdontologoForm(FormularioBase):
    class Meta:
        model = Odontologo
        fields = ['nombres', 'apellidos', 'numero_colegiatura', 'especialidad', 'telefono', 'correo', 'estado']


class CitaForm(FormularioBase):
    class Meta:
        model = Cita
        fields = ['paciente', 'odontologo', 'fecha', 'hora', 'motivo', 'estado', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d'),
            'hora': forms.TimeInput(format='%H:%M'),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }


class DiagnosticoForm(FormularioBase):
    class Meta:
        model = Diagnostico
        fields = ['cita', 'fecha', 'descripcion', 'recomendaciones']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d'),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'recomendaciones': forms.Textarea(attrs={'rows': 3}),
        }


class TratamientoForm(FormularioBase):
    class Meta:
        model = Tratamiento
        fields = ['diagnostico', 'nombre', 'costo', 'fecha_inicio', 'fecha_fin', 'estado', 'descripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d'),
            'fecha_fin': forms.DateInput(format='%Y-%m-%d'),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class RecetaForm(FormularioBase):
    class Meta:
        model = Receta
        fields = ['diagnostico', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'fecha_emision', 'indicaciones']
        widgets = {
            'fecha_emision': forms.DateInput(format='%Y-%m-%d'),
            'indicaciones': forms.Textarea(attrs={'rows': 3}),
        }


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    codigo = forms.CharField(
        label='Código de invitación (solo en producción)',
        required=False,
        widget=forms.PasswordInput,
        help_text='En desarrollo se puede dejar vacío; en producción es obligatorio.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def clean_codigo(self):
        from django.utils.crypto import constant_time_compare
        codigo = self.cleaned_data.get('codigo', '')
        if not settings.DEBUG and not constant_time_compare(codigo, settings.REGISTRATION_CODE):
            raise forms.ValidationError('Código de invitación no válido.')
        return codigo
