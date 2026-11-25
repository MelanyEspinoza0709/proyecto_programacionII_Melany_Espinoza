# Luxury Parking

Luxury Parking es una aplicación web para administrar información de un
estacionamiento. Permite gestionar clientes, vehículos y estancias, consultar
servicios y registrar la salida de un vehículo.

## Objetivo

El objetivo del sistema es ayudar a una recepcionista a registrar los vehículos
que ingresan, asociarles servicios y finalizar sus estancias al momento de la
salida. También permite administrar clientes, vehículos y cuentas con distintos
permisos.

## Tecnologías

- Python 3.14.3 y Django 6.1.3, versiones observadas en el entorno virtual del
  proyecto.
- SQLite como base de datos local.
- HTML para las páginas y CSS propio para el diseño.
- `requirements.txt` fija Django en la versión `6.1.3`.

## Estructura del proyecto

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
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── cargar_datos.py
│   │       └── configurar_grupos.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cliente.py
│   │   ├── estancia.py
│   │   ├── servicio.py
│   │   └── vehiculo.py
│   ├── static/estacionamiento/css/estilos.css
│   ├── templates/estacionamiento/
│   │   ├── autenticacion/
│   │   ├── clientes/
│   │   ├── estancias/
│   │   ├── espacios/
│   │   ├── servicios/
│   │   ├── vehiculos/
│   │   └── base.html
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

La carpeta `.venv` contiene el entorno virtual local y está excluida del
repositorio por `.gitignore`.

## Modelos y relaciones

- **Cliente:** guarda nombre, apellido, cédula, teléfono y correo. La cédula es
  única.
- **Vehiculo:** guarda marca, modelo, año, placa y color. Su relación
  `ForeignKey` vincula cada vehículo con un cliente; la placa es única.
- **Estancia:** guarda el vehículo, el espacio, fechas de entrada y salida,
  estado y total. También guarda el usuario que la creó. Se relaciona con
  `Vehiculo` y con el usuario mediante `ForeignKey`.
- **Servicio:** guarda nombre, descripción y precio. Tiene una relación
  `ManyToMany` con `Estancia`: una estancia puede tener varios servicios y un
  servicio puede estar asociado a varias estancias.

Los estados de una estancia son `ACTIVA`, `FINALIZADA` y `CANCELADA`. Las fechas
se guardan en campos de fecha y hora y los precios y totales en campos decimales.

## Funcionalidades y módulos

| Módulo | Funcionalidad |
| --- | --- |
| Clientes | Crear, listar, consultar, editar y eliminar clientes. |
| Vehículos | Crear, listar, consultar, editar y eliminar vehículos. |
| Estancias | Registrar entradas, listar y consultar estancias, editar o eliminar según permisos y registrar salidas. |
| Servicios | Listar servicios y ver sus detalles. Las vistas disponibles actuales no implementan un CRUD de servicios. |
| Espacios | Listar espacios usados en las estancias y consultar sus estancias y ocupación. |
| Autenticación | Registrar cuentas, iniciar sesión y cerrar sesión. |
| Administración | Modelos Cliente, Vehiculo, Estancia y Servicio registrados en el administrador de Django. |

El formulario de estancia permite seleccionar varios servicios y muestra el
precio junto al nombre de cada uno. El formulario de cliente valida que la
cédula tenga exactamente diez dígitos.

### Cálculo del total de una estancia

Al registrar la salida, el sistema calcula el tiempo desde la entrada y cobra
$2.00 por cada hora iniciada, con un mínimo de una hora. Luego suma los precios
de los servicios asociados, guarda el total y cambia el estado a `FINALIZADA`.

Ejemplo: una permanencia de 2 horas y 20 minutos se cobra como 3 horas:
3 × $2.00 = $6.00. Si los servicios suman $15.00, el total es $21.00.

## Registro, inicio de sesión y grupos

Las rutas de autenticación son `/registro/`, `/login/` y `/logout/`. El cierre
de sesión se envía mediante POST. Al registrarse, la aplicación agrega la cuenta
nueva al grupo `Recepcionistas`.

El comando `configurar_grupos` crea y asigna los permisos siguientes:

- **Administradores:** permisos de consulta, creación, modificación y
  eliminación para los cuatro modelos.
- **Recepcionistas:** permisos de consulta, creación y modificación para los
  cuatro modelos; no reciben permisos de eliminación.

Las vistas también comprueban los permisos al recibir una URL directa. Para
editar, eliminar o registrar la salida de una estancia, la persona debe ser
quien creó esa estancia o ser superusuario. Pertenecer a Administradores no
omite por sí solo esta comprobación de propiedad.

El comando que crea los grupos no crea usuarios. Las cuentas observadas en la
base local revisada son:

| Usuario | Rol observado |
| --- | --- |
| `melany` | Superusuario y miembro del personal de Django; no pertenece a un grupo. |
| `admin_luxury` | Miembro de Administradores; no es superusuario. |
| `Lucia` | Miembro de Recepcionistas. |
| `usuario_datos_demo` | Cuenta usada por `cargar_datos` para registrar las estancias de ejemplo; sin grupo. El comando le asigna una contraseña inutilizable cuando crea esa cuenta. |

Estos nombres describen la base local revisada y pueden ser distintos en otra
instalación. No se incluyen contraseñas porque no se documentan aquí.
Al instalar el proyecto desde cero, las cuentas de la base local no se crean
automáticamente. El comando `configurar_grupos` crea grupos y asigna permisos,
pero no crea usuarios; `cargar_datos` asegura la cuenta `usuario_datos_demo` y
los datos de ejemplo. El registro crea una cuenta cuando alguien completa el
formulario y la agrega a Recepcionistas. `createsuperuser` crea un superusuario.
La pertenencia de una cuenta al grupo Administradores no se asigna
automáticamente por estos comandos.

Las pruebas automatizadas crean además cuentas temporales en su base de prueba;
no son las cuentas persistentes de `db.sqlite3`:

- `recepcionista`: se agrega al grupo temporal Recepcionistas con permisos de
  consulta, creación y cambio de clientes.
- `recepcionista_estancias`: recibe permisos directos para consultar, crear y
  cambiar estancias; la prueba no lo agrega a un grupo.

No se documentan contraseñas para estas cuentas temporales.

## Requisitos

- Windows con PowerShell.
- Python 3.14.3, usado por el entorno virtual revisado.
- Las dependencias indicadas en `requirements.txt` (Django 6.1.3).

## Instalación y ejecución

Abre PowerShell en la carpeta que contiene `Estacionamiento` y ejecuta:

```powershell
cd .\Estacionamiento
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py configurar_grupos
python manage.py cargar_datos
python manage.py runserver
```

La migración prepara las tablas. `configurar_grupos` debe ejecutarse después de
las migraciones para que los permisos de los grupos queden asignados.
`createsuperuser` es un comando interactivo de Django: ejecútalo después de
migrar si necesitas crear una cuenta para ingresar al panel `/admin/`. Solicita
los datos de la cuenta en la terminal; este README no incluye contraseñas.
`cargar_datos` usa `get_or_create` para proporcionar datos de ejemplo de
clientes, vehículos, estancias y servicios. El comando crea cinco ejemplos de
cada uno de esos modelos cuando no existen ya.

Cuando el servidor esté en ejecución, abre `http://127.0.0.1:8000/`. Si PowerShell
no permite activar el entorno virtual, se puede invocar directamente
`.\.venv\Scripts\python.exe` en lugar de `python`.

## Panel de administración

El panel está disponible en `/admin/` y los cuatro modelos están registrados.
Para entrar se necesita una cuenta con acceso al administrador de Django. En la
base local revisada, `melany` es superusuario; `admin_luxury` pertenece al grupo
Administradores, pero no es superusuario ni miembro del personal de Django.

## Pruebas automatizadas

Para ejecutar las pruebas desde la carpeta del proyecto:

```powershell
python manage.py test
```

`estacionamiento/tests.py` contiene pruebas para las páginas de registro e
inicio de sesión, permisos básicos de clientes y el registro de salida de una
estancia. La prueba de salida verifica selección múltiple de servicios, CSRF,
estado final y cálculo del total.

## Configuración de desarrollo

La configuración actual usa SQLite y está preparada para desarrollo local.
`DEBUG` está activado y `ALLOWED_HOSTS` está vacío. Antes de publicar el
proyecto, configura una clave secreta segura, `DEBUG`, `ALLOWED_HOSTS` y los
demás ajustes apropiados para producción.
