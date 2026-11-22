# Consultorio Odontológico «Sonrisa Perfecta» — Django + MariaDB

Sistema web integral para la gestión de pacientes y atención odontológica, desarrollado en **Python**, **Django**, **MariaDB/MySQL**, **HTML5**, **CSS3** y **JavaScript**, tomando como referencia la arquitectura profesional del proyecto base y respetando estrictamente el diseño visual y tipografía estándar (16 px) sin librerías externas pesadas (sin Bootstrap).

---

## 📋 Características y Requisitos Implementados

1. **Siete Modelos de Negocio en Archivos Independientes (`apps/models/`):**
   - `Paciente.py`: Registro de pacientes (nombres, apellidos, DNI con validación de 8 dígitos, fecha de nacimiento, teléfono, dirección, correo, fecha de registro automática).
   - `Odontologo.py`: Cirujanos dentistas (nombres, apellidos, colegiatura COP, teléfono, correo, relación con Especialidad, estado Activo/Inactivo).
   - `Especialidad.py`: Especialidades odontológicas (nombre, descripción, estado Activa/Inactiva).
   - `Cita.py`: Citas odontológicas (relación con Paciente y Odontólogo, fecha, hora, motivo de consulta, estado, observaciones).
   - `Diagnostico.py`: Diagnósticos clínicos (relación con Cita, descripción, recomendaciones, fecha del diagnóstico).
   - `Tratamiento.py`: Procedimientos y tratamientos (relación con Diagnóstico, nombre, descripción, fecha inicio, fecha fin, costo, estado).
   - `Receta.py`: Prescripciones médicas odontológicas (relación con Diagnóstico, medicamento, dosis, frecuencia, duración, indicaciones, fecha de emisión).
   - `__init__.py`: Exportación centralizada de modelos.

2. **Operaciones CRUD Completas:**
   - Registrar, listar, buscar en tiempo real, editar y eliminar con protección de integridad referencial para las siete tablas.

3. **Autenticación y Seguridad:**
   - Login con enlace de registro y checkbox **«Mantener mi cuenta abierta»** (sesión extendida a 14 días o expiración al cerrar el navegador).
   - Protección de datos clínicos confidenciales y manejo de variables de entorno mediante `.env`.

4. **Dashboard Principal:**
   - Tarjetas de indicadores numéricos para Pacientes, Citas, Tratamientos y Diagnósticos (además de Odontólogos, Especialidades y Recetas).
   - Tabla interactiva de citas recientes con acceso rápido a creación de citas.

5. **Reportes Filtrables y Fichas Imprimibles:**
   - Reportes dinámicos filtrables por rango de fechas (`desde` y `hasta`) y estado para: **Citas**, **Diagnósticos**, **Tratamientos** y **Recetas**.
   - Función de impresión directa y guardado en PDF (`window.print()`).
   - Fichas individuales imprimibles con membrete oficial del consultorio para cada cita, diagnóstico, tratamiento y receta médica.

6. **Diseño y Estilo:**
   - Diseño adaptable (responsive) para escritorio y móviles.
   - Tipografía base de 16 px sin uso de Bootstrap.

---

## 🚀 Instalación y Puesta en Marcha (Windows / PowerShell)

1. **Clonar o ubicarse en la carpeta del proyecto:**
   ```powershell
   cd C:\xampp\htdocs\gestion_muela
   ```

2. **Crear o activar el entorno virtual:**
   ```powershell
   py -m venv .venv
   ```

3. **Instalar dependencias:**
   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. **Configurar la base de datos en `.env`:**
   Asegúrate de que el archivo `.env` contenga los datos correctos de tu servidor MySQL/MariaDB (por defecto en XAMPP puerto 3306 o 3307):
   ```env
   DJANGO_DEBUG=1
   DJANGO_SECRET_KEY=admin-secret-key-sonrisa-perfecta-2026
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
   DB_NAME=odontologia_db
   DB_USER=root
   DB_PASSWORD=admin
   DB_HOST=127.0.0.1
   DB_PORT=3307
   ```

5. **Crear la base de datos en phpMyAdmin o MySQL:**
   ```sql
   CREATE DATABASE IF NOT EXISTS odontologia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
   *(También disponible en `database/crear_bd.sql`)*.

6. **Ejecutar migraciones:**
   ```powershell
   .\.venv\Scripts\python.exe manage.py migrate
   ```

7. **Usuario Administrador inicial:**
   - **Usuario:** `admin`
   - **Contraseña:** `admin`
   *(También puedes crear usuarios adicionales con `createsuperuser` o desde la pantalla de Registro)*.

8. **Iniciar el servidor de desarrollo:**
   ```powershell
   .\.venv\Scripts\python.exe manage.py runserver
   ```

9. **Abrir en el navegador:**
   - `http://127.0.0.1:8000/login/`

---

## 🧪 Ejecución de Pruebas Unitarias

Para comprobar el correcto funcionamiento de los 7 modelos, el CRUD, las validaciones de DNI, la autenticación y las vistas de reportes:
```powershell
.\.venv\Scripts\python.exe manage.py test apps
```
