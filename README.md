# Luxury Parking

Luxury Parking es una aplicación web desarrollada con Django para administrar un estacionamiento. Permite gestionar clientes, vehículos, estancias y servicios, además de registrar la entrada y salida de los vehículos.

## 1. Objetivo del proyecto

El objetivo del sistema es facilitar el trabajo de una recepcionista al registrar los vehículos que ingresan al estacionamiento, asociarles servicios y finalizar sus estancias al momento de la salida.

También permite administrar clientes, vehículos y cuentas de usuario mediante diferentes permisos.

## 2. Tecnologías utilizadas

- Python 3.14.3.
- Django 6.1.3.
- SQLite como base de datos local.
- HTML para la estructura de las páginas.
- CSS para el diseño de la aplicación.

Las dependencias del proyecto se encuentran en el archivo `requirements.txt`.

## 3. Estructura del proyecto

```text
Estacionamiento/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── estacionamiento/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── cliente_form.py
│   │   ├── estancia_form.py
│   │   ├── registro_form.py
│   │   ├── servicio_form.py
│   │   └── vehiculo_form.py
│   ├── management/
│   │   └── commands/
│   │       ├── cargar_datos.py
│   │       └── configurar_grupos.py
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cliente.py
│   │   ├── estancia.py
│   │   ├── servicio.py
│   │   └── vehiculo.py
│   ├── static/
│   │   └── estacionamiento/css/estilos.css
│   ├── templates/
│   │   └── estacionamiento/
│   │       ├── autenticacion/
│   │       ├── clientes/
│   │       ├── estancias/
│   │       ├── espacios/
│   │       ├── servicios/
│   │       ├── vehiculos/
│   │       └── base.html
│   ├── urls/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── cliente.py
│   │   ├── espacio.py
│   │   ├── estancia.py
│   │   ├── servicio.py
│   │   └── vehiculo.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── auth_views.py
│   │   ├── cliente.py
│   │   ├── espacio.py
│   │   ├── estancia.py
│   │   ├── servicio.py
│   │   └── vehiculo.py
│   └── tests.py
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

La carpeta `.venv` contiene el entorno virtual y está excluida del repositorio mediante `.gitignore`.

## 4. Modelos y relaciones

El sistema cuenta con cuatro modelos principales:

- **Cliente:** almacena nombre, apellido, cédula, teléfono y correo electrónico. La cédula es única.
- **Vehiculo:** almacena marca, modelo, año, placa y color. Cada vehículo pertenece a un cliente mediante una relación `ForeignKey`. La placa es única.
- **Estancia:** registra el vehículo, el espacio, las fechas de entrada y salida, el estado y el total a pagar. También guarda el usuario que creó la estancia.
- **Servicio:** almacena nombre, descripción y precio. Se relaciona con Estancia mediante `ManyToManyField`, por lo que una estancia puede tener varios servicios.

### Relaciones entre los modelos

- Cliente 1:N Vehiculo.
- Vehiculo 1:N Estancia.
- Estancia N:M Servicio.
- Usuario 1:N Estancia, mediante el campo que registra quién creó cada estancia.

Los estados de una estancia son `ACTIVA`, `FINALIZADA` y `CANCELADA`.

Las fechas se almacenan en campos de fecha y hora, mientras que los precios y totales utilizan campos decimales.

## 5. Funcionalidades del sistema

| Módulo | Funcionalidad |
|---|---|
| Clientes | Crear, listar, consultar, editar y eliminar clientes. |
| Vehículos | Crear, listar, consultar, editar y eliminar vehículos. |
| Estancias | Registrar entradas, consultar estancias, modificarlas y registrar salidas según los permisos. |
| Servicios | Consultar los servicios y sus detalles. |
| Espacios | Consultar los espacios utilizados y sus estancias. |
| Autenticación | Registrar cuentas, iniciar sesión y cerrar sesión. |
| Administración | Administrar los cuatro modelos desde Django Admin. |

El formulario de estancia permite seleccionar varios servicios y muestra sus precios. El formulario de cliente valida que la cédula tenga exactamente diez dígitos.

### 5.1. Cálculo del total de una estancia

Al registrar la salida de un vehículo, el sistema calcula el tiempo transcurrido desde su entrada y cobra $2.00 por cada hora iniciada, con un mínimo de una hora.

Después suma el precio de los servicios asociados, guarda el total y cambia el estado de la estancia a `FINALIZADA`.

**Ejemplo:**

- Tiempo de permanencia: 2 horas y 20 minutos.
- Cobro del estacionamiento: 3 × $2.00 = $6.00.
- Servicios: $15.00.
- Total: $21.00.

## 6. Autenticación y permisos

Las rutas de autenticación son:

- `/registro/`: registro de usuarios.
- `/login/`: inicio de sesión.
- `/logout/`: cierre de sesión mediante POST.

Cuando una persona se registra, su cuenta se agrega automáticamente al grupo `Recepcionistas`.

El proyecto utiliza dos grupos principales:

### Administradores

Tienen permisos de consulta, creación, modificación y eliminación para los cuatro modelos.

### Recepcionistas

Tienen permisos de consulta, creación y modificación para los cuatro modelos. No reciben permisos de eliminación.

Las vistas también verifican los permisos cuando se intenta ingresar directamente mediante una URL.

Para editar, eliminar o registrar la salida de una estancia, el usuario debe ser quien creó esa estancia o ser superusuario.

Pertenecer al grupo `Administradores` no elimina esta comprobación de propiedad.

## 7. Cuentas de prueba

Las siguientes cuentas corresponden a la base de datos local utilizada durante las pruebas del proyecto.

| Usuario | Rol o grupo | Contraseña |
|---|---|---|
| `melany` | Superusuario y personal de Django | **melanyespinoza123** |
| `admin_luxury` | Grupo Administradores | **luxury1234** |
| `Lucia` | Grupo Recepcionistas | **luciarecepcionista** |
| `usuario_datos_demo` | Usuario de datos de ejemplo, sin grupo | No tiene contraseña utilizable. |

**Importante:**

- `melany` puede ingresar al panel de administración de Django porque es superusuario y miembro del personal.
- `admin_luxury` pertenece al grupo Administradores, pero no es superusuario ni miembro del personal de Django.
- `Lucia` pertenece al grupo Recepcionistas.
- `usuario_datos_demo` es utilizado por el comando de datos de ejemplo para registrar las estancias.

Los nombres y las cuentas anteriores corresponden a la base local revisada. No se crean automáticamente al clonar el repositorio.

El comando `configurar_grupos` crea los grupos y asigna sus permisos, pero no crea las cuentas personales. Para crear un superusuario se utiliza `createsuperuser`. Las demás cuentas pueden registrarse desde la aplicación y recibir su grupo correspondiente desde la administración de Django.

## 8. Requisitos para ejecutar el proyecto

- Windows.
- PowerShell.
- Python 3.14.3.
- Las dependencias indicadas en `requirements.txt`.

## 9. Instalación y ejecución

Primero, clona el repositorio y abre PowerShell en la carpeta del proyecto.

Ejecuta los siguientes comandos:

```powershell
cd .\Estacionamiento
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py configurar_grupos
python manage.py cargar_datos
python manage.py createsuperuser
python manage.py runserver
```

**Descripción de los comandos:**

- `migrate`: crea las tablas necesarias en la base de datos.
- `configurar_grupos`: crea los grupos y configura sus permisos.
- `cargar_datos`: registra datos de ejemplo para clientes, vehículos, estancias y servicios.
- `createsuperuser`: permite crear una cuenta con acceso al panel de administración.
- `runserver`: inicia el servidor de desarrollo.

El comando `cargar_datos` utiliza `get_or_create` para evitar duplicar los registros que ya existen.

Si PowerShell no permite activar el entorno virtual, se puede utilizar directamente:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Cuando el servidor esté iniciado, abre la siguiente dirección:

http://127.0.0.1:8000/

## 10. Panel de administración

El panel de administración está disponible en:

http://127.0.0.1:8000/admin/

Los cuatro modelos principales están registrados en Django Admin:

- Cliente.
- Vehiculo.
- Estancia.
- Servicio.

Para ingresar se necesita una cuenta con acceso al administrador de Django.

## 11. Pruebas automatizadas

Para ejecutar las pruebas del proyecto, utiliza:

```powershell
python manage.py test
```

El archivo `estacionamiento/tests.py` contiene pruebas relacionadas con:

- Registro de usuarios.
- Inicio de sesión.
- Permisos de clientes.
- Registro de salida de una estancia.
- Selección de servicios y cálculo del total.

Las pruebas verifican también el estado final de la estancia y el funcionamiento de las operaciones protegidas.

## 12. Configuración de desarrollo

El proyecto utiliza SQLite y está configurado para ejecutarse en un entorno local de desarrollo.

Actualmente, `DEBUG` está activado y `ALLOWED_HOSTS` está vacío.

Antes de publicar el sistema en un servidor real, se deben configurar una clave secreta segura, `DEBUG`, `ALLOWED_HOSTS` y los demás ajustes necesarios para producción.

## 13. Repositorio

**GitHub:**  
https://github.com/MelanyEspinoza0709/proyecto_programacionII_Melany_Espinoza

**Rama de entrega:**  
`ENTREGA-FINAL-LUXURY-PARKING`