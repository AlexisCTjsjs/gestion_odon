from datetime import date, time
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import (
    Paciente, Especialidad, Odontologo,
    Cita, Diagnostico, Tratamiento, Receta
)


class SonrisaPerfectaTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='dentista', password='ClaveSegura123#')
        self.paciente = Paciente.objects.create(
            nombres='Carlos',
            apellidos='Mendoza',
            dni='72345678',
            fecha_nacimiento=date(1995, 5, 20),
            telefono='987654321',
            direccion='Av. Arequipa 123',
            correo='carlos.mendoza@example.com'
        )
        self.especialidad = Especialidad.objects.create(
            nombre='Ortodoncia',
            descripcion='Corrección de posición dental',
            estado='Activa'
        )
        self.odontologo = Odontologo.objects.create(
            nombres='María',
            apellidos='Vargas',
            numero_colegiatura='COP-4589',
            telefono='912345678',
            correo='maria.vargas@sonrisaperfecta.pe',
            especialidad=self.especialidad,
            estado='Activo'
        )
        self.cita = Cita.objects.create(
            paciente=self.paciente,
            odontologo=self.odontologo,
            fecha=date(2026, 11, 20),
            hora=time(10, 30),
            motivo='Evaluación de brackets',
            estado='Pendiente',
            observaciones='Paciente presenta mordida cruzada'
        )
        self.diag = Diagnostico.objects.create(
            cita=self.cita,
            descripcion='Maloclusión clase II con apiñamiento moderado',
            recomendaciones='Se sugiere alineación con aparatología fija',
            fecha=date(2026, 11, 20)
        )
        self.trat = Tratamiento.objects.create(
            diagnostico=self.diag,
            nombre='Colocación de brackets metálicos',
            descripcion='Instalación de brackets prescripción Roth slot 022',
            fecha_inicio=date(2026, 11, 25),
            fecha_fin=date(2027, 11, 25),
            costo=Decimal('2800.00'),
            estado='En proceso'
        )
        self.receta = Receta.objects.create(
            diagnostico=self.diag,
            medicamento='Ibuprofeno 400 mg',
            dosis='1 tableta',
            frecuencia='Cada 8 horas',
            duracion='3 días',
            indicaciones='Tomar después de los alimentos si hay molestias',
            fecha_emision=date(2026, 11, 20)
        )

    def test_login_requerido(self):
        r = self.client.get(reverse('listado', args=['pacientes']))
        self.assertEqual(r.status_code, 302)

    def test_crud_de_siete_tablas(self):
        self.client.force_login(self.usuario)
        secciones = ['pacientes', 'odontologos', 'especialidades', 'citas', 'diagnosticos', 'tratamientos', 'recetas']
        for seccion in secciones:
            self.assertEqual(self.client.get(reverse('listado', args=[seccion])).status_code, 200)
            self.assertEqual(self.client.get(reverse('nuevo', args=[seccion])).status_code, 200)

        elementos = [
            ('pacientes', self.paciente),
            ('odontologos', self.odontologo),
            ('especialidades', self.especialidad),
            ('citas', self.cita),
            ('diagnosticos', self.diag),
            ('tratamientos', self.trat),
            ('recetas', self.receta),
        ]
        for seccion, obj in elementos:
            self.assertEqual(self.client.get(reverse('editar', args=[seccion, obj.pk])).status_code, 200)

    def test_reportes_e_impresiones(self):
        self.client.force_login(self.usuario)
        # Acceso a reportes
        self.assertEqual(self.client.get(reverse('reporte')).status_code, 200)
        for tipo in ['citas', 'diagnosticos', 'tratamientos', 'recetas']:
            self.assertEqual(self.client.get(reverse('reporte_tipo', args=[tipo])).status_code, 200)

        imprimibles = [
            ('citas', self.cita),
            ('diagnosticos', self.diag),
            ('tratamientos', self.trat),
            ('recetas', self.receta),
        ]
        for seccion, obj in imprimibles:
            self.assertEqual(self.client.get(reverse('imprimir', args=[seccion, obj.pk])).status_code, 200)

    def test_eliminar_no_permitido_por_get(self):
        self.client.force_login(self.usuario)
        self.assertEqual(self.client.get(reverse('eliminar', args=['recetas', self.receta.pk])).status_code, 405)

    def test_no_eliminar_registro_con_dependencias(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(reverse('eliminar', args=['pacientes', self.paciente.pk]))
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Paciente.objects.filter(pk=self.paciente.pk).exists())

    def test_crear_paciente_y_eliminar_sin_dependencias(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(reverse('nuevo', args=['pacientes']), {
            'nombres': 'Lucía',
            'apellidos': 'Torres',
            'dni': '87654321',
            'fecha_nacimiento': '2000-01-15',
            'telefono': '999888777',
            'direccion': 'Calle Lima 456',
            'correo': 'lucia.torres@example.com'
        })
        self.assertEqual(respuesta.status_code, 302)
        nuevo_paciente = Paciente.objects.get(dni='87654321')
        self.assertIsNotNone(nuevo_paciente)

        self.assertEqual(self.client.post(reverse('eliminar', args=['pacientes', nuevo_paciente.pk])).status_code, 302)
        self.assertFalse(Paciente.objects.filter(dni='87654321').exists())

    def test_validacion_dni(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(reverse('nuevo', args=['pacientes']), {
            'nombres': 'Invalido',
            'apellidos': 'Test',
            'dni': '123',
            'fecha_nacimiento': '2000-01-15',
            'telefono': '999888777',
            'direccion': 'Calle Lima 456',
            'correo': 'invalido@example.com'
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Paciente.objects.filter(correo='invalido@example.com').exists())

    def test_login_recordarme(self):
        respuesta = self.client.post(reverse('login'), {
            'username': 'dentista',
            'password': 'ClaveSegura123#',
            'recordarme': '1'
        })
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(self.client.session.get_expiry_age() // 86400, 14)

    def test_registro_en_desarrollo(self):
        respuesta = self.client.post(reverse('registro'), {
            'username': 'asistente',
            'email': 'asistente@sonrisaperfecta.pe',
            'password1': 'ClaveAsistente123#',
            'password2': 'ClaveAsistente123#'
        })
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(User.objects.filter(username='asistente').exists())
