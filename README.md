# GameLoop — Documentación del proyecto

## 1. Descripción del proyecto

**GameLoop** es una aplicación web desarrollada con Django para una comunidad de videojuegos. La estructura de datos permite gestionar usuarios, perfiles, preferencias, estadísticas, amistades, grupos, juegos, noticias, comentarios, reacciones, chats, mensajes y notificaciones.

El proyecto practica el diseño de modelos relacionales en Django, las relaciones entre entidades, la creación de datos ficticios mediante Faker y las copias de seguridad mediante fixtures JSON.

## 2. Tecnologías utilizadas

- **Python 3:** lenguaje de programación.
- **Django:** framework web y ORM.
- **SQLite:** base de datos predeterminada del proyecto, salvo que `GameLoop/settings.py` indique otra.
- **Faker:** generación de datos ficticios para pruebas.
- **Git y GitHub:** control de versiones y alojamiento del repositorio.

Las dependencias del proyecto se encuentran en `requirements.txt`.

## 3. Repositorio y autores

Autores:
- Alejandro Fernández Linares
- José Manuel Fernández Linares

## 4. Estructura principal

```text
Proyecto_2_DAW/
├── manage.py
├── requirements.txt
├── backup.json
├── .gitignore
├── GameLoop/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── core/
    ├── models.py
    ├── admin.py
    ├── migrations/
    └── management/
        └── commands/
            └── seed.py
```

- `manage.py`: punto de entrada para los comandos de Django.
- `GameLoop/settings.py`: configuración del proyecto.
- `core/models.py`: definición de los 16 modelos y sus relaciones.
- `core/admin.py`: configuración del sitio de administración.
- `core/migrations/`: migraciones que crean y actualizan el esquema de la base de datos.
- `core/management/commands/seed.py`: comando personalizado para generar datos de prueba.
- `backup.json`: fixture JSON para exportar o importar datos.
- `requirements.txt`: dependencias de Python.

## 5. Modelos y atributos

La aplicación contiene **16 modelos**. En las tablas siguientes se separan los campos de datos de los campos de relación. Los campos de relación (`OneToOneField`, `ForeignKey` y `ManyToManyField`) se documentan en la sección 6.

### 5.1. `Usuario`

Hereda de `AbstractUser` de Django y, por ello, incluye los campos de autenticación habituales, entre ellos `username`, `password`, `email`, `first_name`, `last_name`, `is_active`, `is_staff`, `is_superuser` y `date_joined`, además de los campos y permisos asociados al sistema de usuarios.

| Campo propio | Tipo | Parámetros / finalidad |
|---|---|---|
| `foto_perfil` | `URLField` | `blank=True`; URL de la foto de perfil. |
| `biografia` | `TextField` | `blank=True`; biografía del usuario. |
| `fecha_registro` | `DateTimeField` | `auto_now_add=True`; fecha y hora de creación del registro. |

El método `__str__` devuelve el nombre de usuario.

### 5.2. `PerfilUsuario`

Almacena información pública adicional del usuario.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `nombre_visible` | `CharField` | `max_length=100`, `blank=True`; nombre mostrado en el perfil. |
| `biografia` | `TextField` | `blank=True`; descripción del perfil. |
| `fecha_nacimiento` | `DateField` | `null=True`, `blank=True`; fecha de nacimiento opcional. |
| `web` | `URLField` | `blank=True`; sitio web del usuario. |

También tiene una relación uno a uno con `Usuario`, descrita en la sección 6.

### 5.3. `ConfiguracionUsuario`

Guarda las preferencias de cada usuario.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `tema_oscuro` | `BooleanField` | `default=False`; indica si se usa el tema oscuro. |
| `notificaciones_activadas` | `BooleanField` | `default=True`; activa o desactiva las notificaciones. |
| `idioma` | `CharField` | `max_length=10`, `default="es"`; idioma preferido. |

También tiene una relación uno a uno con `Usuario`.

### 5.4. `EstadisticasUsuario`

Registra estadísticas de actividad relacionadas con un usuario.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `juegos_favoritos` | `PositiveIntegerField` | `default=0`; cantidad de juegos favoritos. |
| `horas_totales` | `FloatField` | `default=0`; horas totales registradas. |
| `nivel` | `PositiveSmallIntegerField` | `default=1`; nivel del usuario. |
| `puntuacion_media` | `DecimalField` | `max_digits=4`, `decimal_places=2`, `default=0`; puntuación media. |

También tiene una relación uno a uno con `Usuario`.

### 5.5. `Amistad`

Representa una solicitud o relación de amistad entre dos usuarios.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `estado` | `CharField` | `max_length=20`, `default="pendiente"`; estado de la solicitud. |
| `fecha_solicitud` | `DateTimeField` | `auto_now_add=True`; fecha de creación. |
| `fecha_aceptacion` | `DateTimeField` | `null=True`, `blank=True`; fecha de aceptación, si existe. |

Tiene dos claves foráneas a `Usuario`: `usuario_origen` y `usuario_destino`.

### 5.6. `Grupo`

Representa una comunidad o grupo de jugadores.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `nombre` | `CharField` | `max_length=100`; nombre del grupo. |
| `descripcion` | `TextField` | `blank=True`; descripción del grupo. |
| `imagen` | `URLField` | `blank=True`; URL de la imagen. |
| `fecha_creacion` | `DateTimeField` | `auto_now_add=True`; fecha de creación. |

Incluye una relación muchos a muchos con `Usuario` mediante `Pertenencia` y otra relación muchos a muchos con `Juego`.

### 5.7. `Pertenencia`

Es el modelo intermedio entre `Usuario` y `Grupo`. Además de vincular ambos registros, guarda información sobre la pertenencia.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `rol` | `CharField` | `max_length=30`, `default="miembro"`; rol dentro del grupo. |
| `fecha_union` | `DateTimeField` | `auto_now_add=True`; fecha de incorporación. |

Tiene claves foráneas `usuario` y `grupo`. Se utiliza como tabla intermedia con atributos adicionales para la relación `Grupo.usuarios`.

### 5.8. `Juego`

Representa un videojuego del catálogo.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `nombre` | `CharField` | `max_length=100`; nombre del videojuego. |
| `descripcion` | `TextField` | `blank=True`; descripción. |
| `genero` | `CharField` | `max_length=50`; género del juego. |
| `imagen` | `URLField` | `blank=True`; URL de la imagen. |
| `fecha_lanzamiento` | `DateField` | `null=True`, `blank=True`; fecha de lanzamiento opcional. |
| `plataformas` | `CharField` | `max_length=200`, `blank=True`; plataformas disponibles. |

### 5.9. `Noticia`

Almacena noticias sobre videojuegos o grupos.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `titulo` | `CharField` | `max_length=200`; título de la noticia. |
| `contenido` | `TextField` | Contenido completo de la noticia. |
| `fecha_publicacion` | `DateTimeField` | `auto_now_add=True`; fecha de creación. |

También contiene claves foráneas a `Usuario` (`autor`), `Grupo` (`grupo`, opcional) y `Juego` (`juego`).

### 5.10. `Comentario`

Representa un comentario publicado sobre una noticia.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `contenido` | `TextField` | Texto del comentario. |
| `fecha` | `DateTimeField` | `auto_now_add=True`; fecha de creación. |

Tiene claves foráneas a `Usuario` y `Noticia`.

### 5.11. `Reaccion`

Registra la reacción de un usuario ante una noticia.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `tipo` | `CharField` | `max_length=20`, `choices=TIPO_CHOICES`; admite `me_gusta` o `no_me_gusta`. |
| `fecha` | `DateTimeField` | `auto_now_add=True`; fecha de creación. |

Tiene claves foráneas a `Usuario` y `Noticia`.

### 5.12. `UsuarioJuego`

Guarda la relación de actividad de un usuario con un videojuego, junto con datos adicionales.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `horas_jugadas` | `FloatField` | `default=0`; horas jugadas. |
| `favorito` | `BooleanField` | `default=False`; indica si el juego es favorito. |
| `fecha_inicio` | `DateField` | `null=True`, `blank=True`; fecha en la que comenzó a jugar. |

Tiene claves foráneas a `Usuario` y `Juego`. Este modelo almacena datos adicionales de la asociación usuario-juego.

### 5.13. `Chat`

Representa una conversación privada o grupal.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `tipo` | `CharField` | `max_length=10`, `choices=TIPO_CHOICES`; admite `privado` o `grupal`. |
| `fecha_creacion` | `DateTimeField` | `auto_now_add=True`; fecha de creación. |
| `nombre` | `CharField` | `max_length=100`, `blank=True`; nombre opcional del chat. |

Tiene una relación muchos a muchos con `Usuario` a través de `ParticipanteChat`.

### 5.14. `ParticipanteChat`

Es el modelo intermedio que vincula usuarios y chats, guardando datos de participación.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `fecha_union` | `DateTimeField` | `auto_now_add=True`; fecha de incorporación al chat. |
| `rol` | `CharField` | `max_length=30`, `default="miembro"`; rol del participante. |

Tiene claves foráneas a `Usuario` y `Chat`. Es la tabla intermedia con atributos adicionales de `Chat.participantes`.

### 5.15. `Mensaje`

Almacena los mensajes de una conversación.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `contenido` | `TextField` | Texto del mensaje. |
| `fecha_envio` | `DateTimeField` | `auto_now_add=True`; fecha de creación. |

Tiene claves foráneas a `Usuario` (`autor`) y `Chat`.

### 5.16. `Notificacion`

Guarda notificaciones dirigidas a los usuarios.

| Campo | Tipo | Parámetros / finalidad |
|---|---|---|
| `tipo` | `CharField` | `max_length=20`, `choices=TIPO_CHOICES`; admite `amistad`, `comentario`, `mensaje` o `grupo`. |
| `mensaje` | `TextField` | Texto descriptivo de la notificación. |
| `fecha` | `DateTimeField` | `auto_now_add=True`; fecha de creación. |
| `leida` | `BooleanField` | `default=False`; indica si se ha leído. |

Tiene una clave foránea a `Usuario`.

> **Nota sobre los campos automáticos:** Django añade una clave primaria `id` automáticamente cuando no se declara otra. `Usuario` también hereda campos del modelo `AbstractUser`. Las claves foráneas y las relaciones muchos a muchos se explican por separado, porque son relaciones entre modelos y no atributos simples de datos.

## 6. Relaciones entre los modelos

### 6.1. Relaciones uno a uno (`OneToOneField`)

| Modelo relacionado | Campo de relación | Significado |
|---|---|---|
| `Usuario` — `PerfilUsuario` | `PerfilUsuario.usuario` | Un usuario tiene como máximo un perfil y cada perfil corresponde a un usuario. |
| `Usuario` — `ConfiguracionUsuario` | `ConfiguracionUsuario.usuario` | Un usuario tiene como máximo un registro de configuración. |
| `Usuario` — `EstadisticasUsuario` | `EstadisticasUsuario.usuario` | Un usuario tiene como máximo un registro de estadísticas. |

En estas relaciones se usa `on_delete=models.CASCADE`, de modo que al eliminar el usuario se elimina el registro dependiente.

### 6.2. Relaciones muchos a uno (`ForeignKey`)

| Modelo que contiene la clave foránea | Campo | Apunta a |
|---|---|---|
| `Amistad` | `usuario_origen` | `Usuario` |
| `Amistad` | `usuario_destino` | `Usuario` |
| `Noticia` | `autor` | `Usuario` |
| `Noticia` | `grupo` | `Grupo` (opcional) |
| `Noticia` | `juego` | `Juego` |
| `Comentario` | `usuario` | `Usuario` |
| `Comentario` | `noticia` | `Noticia` |
| `Reaccion` | `usuario` | `Usuario` |
| `Reaccion` | `noticia` | `Noticia` |
| `Pertenencia` | `usuario` | `Usuario` |
| `Pertenencia` | `grupo` | `Grupo` |
| `UsuarioJuego` | `usuario` | `Usuario` |
| `UsuarioJuego` | `juego` | `Juego` |
| `ParticipanteChat` | `usuario` | `Usuario` |
| `ParticipanteChat` | `chat` | `Chat` |
| `Mensaje` | `autor` | `Usuario` |
| `Mensaje` | `chat` | `Chat` |
| `Notificacion` | `usuario` | `Usuario` |

Una clave foránea permite que varios registros del modelo que la contiene apunten al mismo registro del modelo relacionado.

### 6.3. Relaciones muchos a muchos (`ManyToManyField`)

| Modelo | Campo | Modelo relacionado | Tabla intermedia |
|---|---|---|---|
| `Grupo` | `usuarios` | `Usuario` | `Pertenencia` (`through="Pertenencia"`) |
| `Chat` | `participantes` | `Usuario` | `ParticipanteChat` (`through="ParticipanteChat"`) |
| `Grupo` | `juegos` | `Juego` | Tabla intermedia automática de Django |

`Pertenencia` contiene los campos extra `rol` y `fecha_union`. `ParticipanteChat` contiene `fecha_union` y `rol`. Por tanto, las relaciones de usuarios con grupos y de usuarios con chats usan modelos intermedios explícitos con atributos adicionales.

`UsuarioJuego` también guarda una asociación entre `Usuario` y `Juego` con `horas_jugadas`, `favorito` y `fecha_inicio`, pero en el código actual está definido como un modelo con dos `ForeignKey`; no está conectado a un `ManyToManyField` mediante `through`.

### 6.4. Comportamiento de `on_delete`

En las claves foráneas y relaciones uno a uno se utiliza `on_delete=models.CASCADE`. Esto significa que al borrar el objeto relacionado, Django elimina los registros dependientes asociados a él.

## 7. Tipos de campos distintos utilizados

Los campos de relación no se cuentan como tipos de atributos simples. En los modelos actuales se utilizan, entre otros, estos tipos:

| Tipo de campo | Ejemplo en el proyecto | Uso |
|---|---|---|
| `CharField` | `Usuario.username`, `Juego.nombre` | Texto corto con longitud máxima. |
| `TextField` | `Usuario.biografia`, `Noticia.contenido` | Texto largo. |
| `URLField` | `Usuario.foto_perfil`, `PerfilUsuario.web` | Dirección URL. |
| `DateField` | `PerfilUsuario.fecha_nacimiento` | Fecha sin hora. |
| `DateTimeField` | `Usuario.fecha_registro`, `Mensaje.fecha_envio` | Fecha y hora. |
| `BooleanField` | `ConfiguracionUsuario.tema_oscuro` | Valor verdadero/falso. |
| `PositiveIntegerField` | `EstadisticasUsuario.juegos_favoritos` | Entero no negativo. |
| `PositiveSmallIntegerField` | `EstadisticasUsuario.nivel` | Entero pequeño no negativo. |
| `FloatField` | `EstadisticasUsuario.horas_totales` | Número de coma flotante. |
| `DecimalField` | `EstadisticasUsuario.puntuacion_media` | Decimal con precisión definida. |
| `EmailField` | `Usuario.email` (heredado de `AbstractUser`) | Dirección de correo electrónico. |

Así, el proyecto utiliza al menos diez tipos distintos de campos no relacionales, contando los campos de autenticación heredados por `Usuario`.

## 8. Parámetros de los campos

| Parámetro | Uso en el proyecto |
|---|---|
| `max_length` | Limita la longitud de campos de texto, por ejemplo `Juego.nombre`. |
| `blank=True` | Permite dejar el campo vacío en formularios y validación. |
| `null=True` | Permite almacenar `NULL` en la base de datos. |
| `default` | Define un valor predeterminado, por ejemplo `tema_oscuro=False`. |
| `auto_now_add=True` | Guarda automáticamente la fecha y hora de creación. |
| `on_delete=models.CASCADE` | Elimina los registros dependientes al borrar el objeto relacionado. |
| `related_name` | Define el nombre de acceso inverso a una relación. |
| `max_digits` | Número máximo de dígitos de un `DecimalField`. |
| `decimal_places` | Número de posiciones decimales de un `DecimalField`. |
| `choices` | Restringe un campo a opciones declaradas, como los tipos de reacción. |
| `through` | Especifica un modelo intermedio para una relación muchos a muchos. |

`blank` y `null` no son equivalentes: `blank` afecta a la validación y `null` al almacenamiento en la base de datos.

## 9. Diagrama entidad-relación

El diagrama entidad-relación debe mostrar los modelos principales, las claves foráneas y las relaciones uno a uno, uno a muchos y muchos a muchos, incluidos los modelos intermedios `Pertenencia` y `ParticipanteChat`.

Imágenes del diagrama incluidas en el repositorio:

<img width="907" height="566" alt="Diagrama entidad-relación de GameLoop" src="https://github.com/user-attachments/assets/f5cd8065-c805-4d33-91ed-821d6e92098d" />

<img width="907" height="566" alt="Diagrama entidad-relación de GameLoop (detalle)" src="https://github.com/user-attachments/assets/3b6c5201-af7a-4abf-82be-824a65c69b4a" />

## 10. Generación de datos de prueba con `seed`

El proyecto incluye un comando de administración personalizado en:

```text
core/management/commands/seed.py
```

Se ejecuta desde la carpeta que contiene `manage.py`:

```bash
python manage.py seed
```

El comando usa **Faker con configuración española** (`Faker("es_ES")`) y la biblioteca `random` para generar valores ficticios. Crea **10 registros nuevos de cada uno de los 16 modelos por ejecución**, incluyendo usuarios, perfiles, configuraciones, estadísticas, juegos, grupos, pertenencias, amistades, noticias, comentarios, reacciones, asociaciones usuario-juego, chats, participantes, mensajes y notificaciones.

El comando crea relaciones entre los datos para que se puedan probar las claves foráneas y las relaciones muchos a muchos. Por ejemplo, cada grupo se asocia con un juego, se crean pertenencias de usuarios a grupos y se asignan participantes a chats.

Las contraseñas de los usuarios de prueba creados por el comando son:

```text
GameLoopDemo123!
```

**Aviso:** este comando añade datos cada vez que se ejecuta; no vacía automáticamente la base de datos. Los nombres de usuario y correos se generan para evitar colisiones. La contraseña indicada es solo para desarrollo y no debe usarse en producción.

## 11. Instalación y ejecución

### 11.1. Crear y activar un entorno virtual

Desde la raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell, la activación es:

```powershell
.venv\Scripts\Activate.ps1
```

### 11.2. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 11.3. Aplicar migraciones

```bash
python manage.py migrate
```

Si se han modificado los modelos y no existen migraciones para esos cambios, primero ejecutar:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 11.4. Crear datos de prueba

```bash
python manage.py seed
```

### 11.5. Crear un usuario administrador (opcional)

```bash
python manage.py createsuperuser
```

### 11.6. Iniciar el servidor

```bash
python manage.py runserver
```

La aplicación se sirve localmente en `http://127.0.0.1:8000/`. El panel de administración se encuentra en `http://127.0.0.1:8000/admin/`.

## 12. Copias de seguridad mediante fixtures

Django permite exportar e importar datos usando fixtures en formato JSON.

### 12.1. Crear una copia

Para exportar los datos a `backup.json`:

```bash
python manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --exclude=contenttypes \
  --exclude=auth.permission \
  --exclude=sessions \
  --indent 2 \
  -o backup.json
```

Este comando genera un archivo JSON con los datos exportados, excluyendo los modelos indicados.

### 12.2. Restaurar una copia

Después de aplicar las migraciones, cargar los datos con:

```bash
python manage.py loaddata backup.json
```

La restauración debe probarse en una base de datos compatible. Si se importan datos en una base que ya contiene registros, pueden aparecer duplicados o conflictos de claves únicas.

## 13. Control de versiones y `.gitignore`

El repositorio debe incluir los archivos necesarios para instalar y ejecutar el proyecto, como el código fuente, las migraciones, `requirements.txt`, la documentación y el fixture que se decida entregar.

Se recomienda no subir el entorno virtual (`.venv/` o `venv/`), `__pycache__/`, archivos compilados (`*.py[cod]`), secretos, ni archivos temporales. La inclusión de una base de datos local debe decidirse según las instrucciones de entrega; las migraciones y los fixtures necesarios no deben eliminarse por error.

Las ramas del proyecto se gestionan con Git. Antes de entregar, comprobar que los cambios están confirmados y subidos a GitHub en las ramas requeridas por la asignatura.

## 14. Conclusión

GameLoop organiza los datos de una comunidad de videojuegos en 16 modelos y utiliza relaciones uno a uno, uno a muchos y muchos a muchos. Los modelos intermedios `Pertenencia` y `ParticipanteChat` permiten añadir atributos a relaciones muchos a muchos. El comando `seed` genera datos ficticios para probar el modelo de datos y los fixtures de Django permiten exportar y restaurar información.

Esta estructura facilita demostrar el diseño de modelos, los tipos y parámetros de campos, las relaciones entre entidades, la generación de datos y las copias de seguridad en Django.
