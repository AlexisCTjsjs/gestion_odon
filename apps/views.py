from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    PacienteForm, EspecialidadForm, OdontologoForm,
    CitaForm, DiagnosticoForm, TratamientoForm, RecetaForm,
    RegistroForm
)
from .models import (
    Paciente, Especialidad, Odontologo,
    Cita, Diagnostico, Tratamiento, Receta
)

SECCIONES = {
    'pacientes': {
        'modelo': Paciente,
        'formulario': PacienteForm,
        'titulo': 'Pacientes',
        'campos': ['apellidos', 'nombres', 'dni', 'telefono', 'correo']
    },
    'odontologos': {
        'modelo': Odontologo,
        'formulario': OdontologoForm,
        'titulo': 'Odontólogos',
        'campos': ['apellidos', 'nombres', 'numero_colegiatura', 'especialidad', 'telefono', 'estado']
    },
    'especialidades': {
        'modelo': Especialidad,
        'formulario': EspecialidadForm,
        'titulo': 'Especialidades',
        'campos': ['nombre', 'descripcion', 'estado']
    },
    'citas': {
        'modelo': Cita,
        'formulario': CitaForm,
        'titulo': 'Citas',
        'campos': ['paciente', 'odontologo', 'fecha', 'hora', 'motivo', 'estado']
    },
    'diagnosticos': {
        'modelo': Diagnostico,
        'formulario': DiagnosticoForm,
        'titulo': 'Diagnósticos',
        'campos': ['cita', 'fecha', 'descripcion', 'recomendaciones']
    },
    'tratamientos': {
        'modelo': Tratamiento,
        'formulario': TratamientoForm,
        'titulo': 'Tratamientos',
        'campos': ['diagnostico', 'nombre', 'costo', 'fecha_inicio', 'fecha_fin', 'estado']
    },
    'recetas': {
        'modelo': Receta,
        'formulario': RecetaForm,
        'titulo': 'Recetas',
        'campos': ['diagnostico', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'fecha_emision']
    },
}

BUSQUEDAS = {
    'pacientes': ['nombres', 'apellidos', 'dni', 'telefono', 'correo'],
    'odontologos': ['nombres', 'apellidos', 'numero_colegiatura', 'especialidad__nombre', 'telefono'],
    'especialidades': ['nombre', 'descripcion'],
    'citas': ['paciente__nombres', 'paciente__apellidos', 'paciente__dni', 'odontologo__nombres', 'odontologo__apellidos', 'motivo'],
    'diagnosticos': ['descripcion', 'recomendaciones', 'cita__paciente__nombres', 'cita__paciente__apellidos', 'cita__paciente__dni'],
    'tratamientos': ['nombre', 'descripcion', 'diagnostico__cita__paciente__nombres', 'diagnostico__cita__paciente__apellidos'],
    'recetas': ['medicamento', 'dosis', 'indicaciones', 'diagnostico__cita__paciente__nombres', 'diagnostico__cita__paciente__apellidos'],
}


def ingresar(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    formulario = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        login(request, formulario.get_user())
        if not request.POST.get('recordarme'):
            request.session.set_expiry(0)  # Cierra al terminar la sesión del navegador
        else:
            request.session.set_expiry(60 * 60 * 24 * 14)  # 14 días
        return redirect('inicio')
    return render(request, 'control/login.html', {
        'formulario': formulario,
        'registro_abierto': settings.REGISTRATION_OPEN
    })


def registro(request):
    if not settings.REGISTRATION_OPEN:
        raise Http404('Registro deshabilitado. Contacta al administrador.')
    if request.user.is_authenticated:
        return redirect('inicio')
    formulario = RegistroForm(request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        usuario = formulario.save(commit=False)
        usuario.email = formulario.cleaned_data['email']
        usuario.save()
        login(request, usuario)
        request.session.set_expiry(0)
        messages.success(request, 'Cuenta creada correctamente. ¡Bienvenido!')
        return redirect('inicio')
    return render(request, 'control/registro.html', {'formulario': formulario})


@login_required
@require_POST
def salir(request):
    logout(request)
    return redirect('login')


@login_required
def inicio(request):
    resumen = [(item['titulo'], item['modelo'].objects.count(), clave) for clave, item in SECCIONES.items()]
    proximas = Cita.objects.select_related('paciente', 'odontologo').order_by('fecha', 'hora')[:8]
    return render(request, 'control/inicio.html', {
        'resumen': resumen,
        'proximas': proximas
    })


@login_required
def listado(request, seccion):
    info = SECCIONES.get(seccion)
    if info is None:
        raise Http404('Sección no disponible')

    objetos = info['modelo'].objects.all()
    if seccion == 'odontologos':
        objetos = objetos.select_related('especialidad')
    elif seccion == 'citas':
        objetos = objetos.select_related('paciente', 'odontologo')
    elif seccion == 'diagnosticos':
        objetos = objetos.select_related('cita__paciente', 'cita__odontologo')
    elif seccion == 'tratamientos':
        objetos = objetos.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo')
    elif seccion == 'recetas':
        objetos = objetos.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo')

    q = request.GET.get('q', '').strip()[:100]
    if q:
        filtro = Q()
        for campo in BUSQUEDAS[seccion]:
            filtro |= Q(**{campo + '__icontains': q})
        objetos = objetos.filter(filtro)

    objetos = objetos[:300]
    filas = [[getattr(obj, campo) for campo in info['campos']] for obj in objetos]
    datos = list(zip(objetos, filas))
    return render(request, 'control/listado.html', {
        'info': info,
        'seccion': seccion,
        'datos': datos,
        'q': q
    })


@login_required
def guardar(request, seccion, pk=None):
    info = SECCIONES.get(seccion)
    if info is None:
        raise Http404('Sección no disponible')

    objeto = get_object_or_404(info['modelo'], pk=pk) if pk else None
    formulario = info['formulario'](request.POST or None, instance=objeto)

    if request.method == 'POST' and formulario.is_valid():
        try:
            formulario.save()
            messages.success(request, 'Registro guardado correctamente.')
            return redirect('listado', seccion=seccion)
        except IntegrityError:
            formulario.add_error(None, 'No se pudo guardar: dato duplicado o relación inválida.')

    return render(request, 'control/formulario.html', {
        'formulario': formulario,
        'info': info,
        'seccion': seccion,
        'objeto': objeto
    })


@login_required
@require_POST
def eliminar(request, seccion, pk):
    info = SECCIONES.get(seccion)
    if info is None:
        raise Http404('Sección no disponible')

    objeto = get_object_or_404(info['modelo'], pk=pk)
    try:
        objeto.delete()
        messages.success(request, 'Registro eliminado correctamente.')
    except ProtectedError:
        messages.error(
            request,
            'No se puede eliminar: tiene registros relacionados dependientes. '
            'Elimine primero los registros asociados.'
        )
    return redirect('listado', seccion=seccion)


@login_required
def imprimir(request, seccion, pk):
    if seccion not in ('citas', 'diagnosticos', 'tratamientos', 'recetas'):
        raise Http404('Documento no disponible')

    modelo = SECCIONES[seccion]['modelo']
    objeto = get_object_or_404(modelo, pk=pk)
    return render(request, 'control/impresion.html', {
        'objeto': objeto,
        'seccion': seccion
    })


@login_required
def reporte(request, tipo=None):
    tipo = tipo or request.GET.get('tipo', 'citas')
    if tipo not in ('citas', 'diagnosticos', 'tratamientos', 'recetas'):
        tipo = 'citas'

    desde = request.GET.get('desde', '').strip()
    hasta = request.GET.get('hasta', '').strip()
    estado = request.GET.get('estado', '').strip()

    fecha_desde = None
    fecha_hasta = None
    try:
        if desde:
            fecha_desde = date.fromisoformat(desde)
        if hasta:
            fecha_hasta = date.fromisoformat(hasta)
    except ValueError:
        messages.error(request, 'Las fechas deben tener formato AAAA-MM-DD.')
        return redirect('reporte_tipo', tipo=tipo)

    estados_disponibles = []
    registros = []

    if tipo == 'citas':
        estados_disponibles = Cita.ESTADOS
        qs = Cita.objects.select_related('paciente', 'odontologo').all()
        if fecha_desde:
            qs = qs.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            qs = qs.filter(fecha__lte=fecha_hasta)
        if estado and estado in dict(Cita.ESTADOS):
            qs = qs.filter(estado=estado)
        registros = qs.order_by('-fecha', '-hora')[:500]

    elif tipo == 'diagnosticos':
        qs = Diagnostico.objects.select_related('cita__paciente', 'cita__odontologo').all()
        if fecha_desde:
            qs = qs.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            qs = qs.filter(fecha__lte=fecha_hasta)
        registros = qs.order_by('-fecha', '-id')[:500]

    elif tipo == 'tratamientos':
        estados_disponibles = Tratamiento.ESTADOS
        qs = Tratamiento.objects.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo').all()
        if fecha_desde:
            qs = qs.filter(fecha_inicio__gte=fecha_desde)
        if fecha_hasta:
            qs = qs.filter(fecha_inicio__lte=fecha_hasta)
        if estado and estado in dict(Tratamiento.ESTADOS):
            qs = qs.filter(estado=estado)
        registros = qs.order_by('-fecha_inicio', '-id')[:500]

    elif tipo == 'recetas':
        qs = Receta.objects.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo').all()
        if fecha_desde:
            qs = qs.filter(fecha_emision__gte=fecha_desde)
        if fecha_hasta:
            qs = qs.filter(fecha_emision__lte=fecha_hasta)
        registros = qs.order_by('-fecha_emision', '-id')[:500]

    return render(request, 'control/reporte.html', {
        'tipo': tipo,
        'registros': registros,
        'desde': desde,
        'hasta': hasta,
        'estado': estado,
        'estados': estados_disponibles,
    })
