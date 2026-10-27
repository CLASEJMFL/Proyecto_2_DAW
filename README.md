# GameLoop — Documentación del proyecto

## 1. Descripción del proyecto

**GameLoop** es una aplicación web desarrollada con Django que permite crear una comunidad de usuarios relacionada con los videojuegos. Incluye perfiles, amistades, grupos, juegos, noticias, comentarios, reacciones, chats, mensajes y notificaciones.

El objetivo es poner en práctica el diseño de modelos, las relaciones entre entidades, la generación de datos de prueba y las copias de seguridad de una aplicación web.

## 2. Tecnologías utilizadas

- **Python 3:** lenguaje de programación.
- **Django:** framework para el desarrollo web.
- **SQLite:** base de datos si se mantiene la configuración predeterminada de Django.
- **Faker:** biblioteca para generar datos ficticios de prueba, si está incluida en las dependencias.
- **Git y GitHub:** control de versiones y alojamiento del código.

## 3. Estructura del proyecto

```text
Proyecto_2_DAW/
├── manage.py
├── requirements.txt
├── backup.json
├── .gitignore
├── core/
│   ├── models.py
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── seed.py
└── ...
```

- `manage.py`: permite ejecutar comandos de administración de Django.
- `requirements.txt`: contiene las dependencias del proyecto.
- `backup.json`: archivo de copia de seguridad de los datos, si está generado y versionado.
- `.gitignore`: excluye archivos locales que no deben incluirse en Git.
- `core/models.py`: contiene los modelos y sus relaciones.
- `core/admin.py`: configura la administración de los modelos.
- `core/management/commands/seed.py`: contiene el comando personalizado para generar datos de prueba.

## 4. Modelos de la aplicación

El proyecto contiene 16 modelos declarados en `core/models.py`.

### 4.1. Usuario

Hereda de `AbstractUser`, por lo que incluye los campos de autenticación proporcionados por Django, como `username`, `first_name`, `last_name`, `email` y `password`.

| Campo propio | Tipo | Parámetros |
|---|---|---|
| `foto_perfil` | `URLField` | `blank=True` |
| `biografia` | `TextField` | `blank=True` |
| `fecha_registro` | `DateTimeField` | `auto_now_add=True` |

Representa a los usuarios registrados en GameLoop.

### 4.2. PerfilUsuario

Almacena información adicional del perfil.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `OneToOneField` | `on_delete=CASCADE`, `related_name="perfil"` |
| `nombre_visible` | `CharField` | `max_length=100`, `blank=True` |
| `biografia` | `TextField` | `blank=True` |
| `fecha_nacimiento` | `DateField` | `null=True`, `blank=True` |
| `web` | `URLField` | `blank=True` |

### 4.3. ConfiguracionUsuario

Guarda las preferencias de cada usuario.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `OneToOneField` | `on_delete=CASCADE`, `related_name="configuracion"` |
| `tema_oscuro` | `BooleanField` | `default=False` |
| `notificaciones_activadas` | `BooleanField` | `default=True` |
| `idioma` | `CharField` | `max_length=10`, `default="es"` |

### 4.4. EstadisticasUsuario

Almacena estadísticas relacionadas con el usuario.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `OneToOneField` | `on_delete=CASCADE`, `related_name="estadisticas"` |
| `juegos_favoritos` | `PositiveIntegerField` | `default=0` |
| `horas_totales` | `FloatField` | `default=0` |
| `nivel` | `PositiveSmallIntegerField` | `default=1` |
| `puntuacion_media` | `DecimalField` | `max_digits=4`, `decimal_places=2`, `default=0` |

### 4.5. Amistad

Representa solicitudes y relaciones de amistad entre usuarios.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario_origen` | `ForeignKey` | `on_delete=CASCADE`, `related_name="amistades_enviadas"` |
| `usuario_destino` | `ForeignKey` | `on_delete=CASCADE`, `related_name="amistades_recibidas"` |
| `estado` | `CharField` | `max_length=20`, `default="pendiente"` |
| `fecha_solicitud` | `DateTimeField` | `auto_now_add=True` |
| `fecha_aceptacion` | `DateTimeField` | `null=True`, `blank=True` |

### 4.6. Grupo

Representa comunidades de usuarios relacionadas con videojuegos.

| Campo | Tipo | Parámetros |
|---|---|---|
| `nombre` | `CharField` | `max_length=100` |
| `descripcion` | `TextField` | `blank=True` |
| `imagen` | `URLField` | `blank=True` |
| `fecha_creacion` | `DateTimeField` | `auto_now_add=True` |
| `usuarios` | `ManyToManyField` | `through="Pertenencia"`, `related_name="grupos"` |
| `juegos` | `ManyToManyField` | `blank=True`, `related_name="grupos"` |

La relación con los usuarios utiliza el modelo intermedio `Pertenencia`. La relación con juegos utiliza la tabla intermedia automática de Django.

### 4.7. Pertenencia

Representa la pertenencia de un usuario a un grupo y almacena información adicional de esa relación.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `grupo` | `ForeignKey` | `on_delete=CASCADE` |
| `rol` | `CharField` | `max_length=30`, `default="miembro"` |
| `fecha_union` | `DateTimeField` | `auto_now_add=True` |

### 4.8. Juego

Representa los videojuegos registrados.

| Campo | Tipo | Parámetros |
|---|---|---|
| `nombre` | `CharField` | `max_length=100` |
| `descripcion` | `TextField` | `blank=True` |
| `genero` | `CharField` | `max_length=50` |
| `imagen` | `URLField` | `blank=True` |
| `fecha_lanzamiento` | `DateField` | `null=True`, `blank=True` |
| `plataformas` | `CharField` | `max_length=200`, `blank=True` |

### 4.9. Noticia

Almacena noticias sobre videojuegos y la comunidad.

| Campo | Tipo | Parámetros |
|---|---|---|
| `titulo` | `CharField` | `max_length=200` |
| `contenido` | `TextField` | Sin parámetros adicionales |
| `fecha_publicacion` | `DateTimeField` | `auto_now_add=True` |
| `autor` | `ForeignKey` | `on_delete=CASCADE` |
| `grupo` | `ForeignKey` | `on_delete=CASCADE`, `null=True`, `blank=True` |
| `juego` | `ForeignKey` | `on_delete=CASCADE` |

El grupo asociado a una noticia es opcional.

### 4.10. Comentario

Representa comentarios publicados en noticias.

| Campo | Tipo | Parámetros |
|---|---|---|
| `contenido` | `TextField` | Sin parámetros adicionales |
| `fecha` | `DateTimeField` | `auto_now_add=True` |
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `noticia` | `ForeignKey` | `on_delete=CASCADE`, `related_name="comentarios"` |

### 4.11. Reaccion

Representa la reacción de un usuario ante una noticia.

| Campo | Tipo | Parámetros |
|---|---|---|
| `tipo` | `CharField` | `max_length=20`, `choices=TIPO_CHOICES` |
| `fecha` | `DateTimeField` | `auto_now_add=True` |
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `noticia` | `ForeignKey` | `on_delete=CASCADE` |

Las opciones de `tipo` son:

- `me_gusta`: Me gusta.
- `no_me_gusta`: No me gusta.

### 4.12. UsuarioJuego

Relaciona a los usuarios con los videojuegos y almacena datos de su actividad.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `juego` | `ForeignKey` | `on_delete=CASCADE` |
| `horas_jugadas` | `FloatField` | `default=0` |
| `favorito` | `BooleanField` | `default=False` |
| `fecha_inicio` | `DateField` | `null=True`, `blank=True` |

### 4.13. Chat

Representa conversaciones privadas o grupales.

| Campo | Tipo | Parámetros |
|---|---|---|
| `tipo` | `CharField` | `max_length=10`, `choices=TIPO_CHOICES` |
| `fecha_creacion` | `DateTimeField` | `auto_now_add=True` |
| `nombre` | `CharField` | `max_length=100`, `blank=True` |
| `participantes` | `ManyToManyField` | `through="ParticipanteChat"`, `related_name="chats"` |

Las opciones de `tipo` son `privado` y `grupal`.

### 4.14. ParticipanteChat

Modelo intermedio que relaciona usuarios y chats.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `chat` | `ForeignKey` | `on_delete=CASCADE` |
| `fecha_union` | `DateTimeField` | `auto_now_add=True` |
| `rol` | `CharField` | `max_length=30`, `default="miembro"` |

### 4.15. Mensaje

Almacena mensajes enviados dentro de los chats.

| Campo | Tipo | Parámetros |
|---|---|---|
| `contenido` | `TextField` | Sin parámetros adicionales |
| `fecha_envio` | `DateTimeField` | `auto_now_add=True` |
| `autor` | `ForeignKey` | `on_delete=CASCADE` |
| `chat` | `ForeignKey` | `on_delete=CASCADE` |

### 4.16. Notificacion

Representa las notificaciones dirigidas a los usuarios.

| Campo | Tipo | Parámetros |
|---|---|---|
| `tipo` | `CharField` | `max_length=20`, `choices=TIPO_CHOICES` |
| `mensaje` | `TextField` | Sin parámetros adicionales |
| `fecha` | `DateTimeField` | `auto_now_add=True` |
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `leida` | `BooleanField` | `default=False` |

Las opciones de `tipo` son `amistad`, `comentario`, `mensaje` y `grupo`.

## 5. Relaciones entre modelos

### 5.1. Uno a uno

Se utiliza `OneToOneField` para establecer una relación exclusiva entre dos registros.

- `Usuario` — `PerfilUsuario`.
- `Usuario` — `ConfiguracionUsuario`.
- `Usuario` — `EstadisticasUsuario`.

Las relaciones utilizan `on_delete=CASCADE`.

### 5.2. Uno a muchos

Se implementan mediante `ForeignKey`.

- `Usuario` → `Amistad`, como usuario de origen y de destino.
- `Usuario` → `Pertenencia`.
- `Grupo` → `Pertenencia`.
- `Usuario`, `Grupo` y `Juego` → `Noticia`.
- `Usuario` y `Noticia` → `Comentario`.
- `Usuario` y `Noticia` → `Reaccion`.
- `Usuario` y `Juego` → `UsuarioJuego`.
- `Usuario` y `Chat` → `ParticipanteChat`.
- `Usuario` y `Chat` → `Mensaje`.
- `Usuario` → `Notificacion`.

### 5.3. Muchos a muchos

Se implementan mediante `ManyToManyField`.

- **Grupo ↔ Usuario:** utiliza el modelo intermedio `Pertenencia`, que almacena `rol` y `fecha_union`.
- **Chat ↔ Usuario:** utiliza el modelo intermedio `ParticipanteChat`, que almacena `fecha_union` y `rol`.
- **Grupo ↔ Juego:** Django genera automáticamente la tabla intermedia.

## 6. Tipos de campos utilizados

En los modelos se utilizan al menos diez tipos de campos diferentes:

| Tipo | Descripción |
|---|---|
| `CharField` | Texto de longitud limitada |
| `TextField` | Texto largo |
| `BooleanField` | Valor verdadero o falso |
| `PositiveIntegerField` | Entero no negativo |
| `PositiveSmallIntegerField` | Entero pequeño no negativo |
| `FloatField` | Número de coma flotante |
| `DecimalField` | Número decimal con precisión definida |
| `DateField` | Fecha |
| `DateTimeField` | Fecha y hora |
| `URLField` | Dirección URL |

El modelo `Usuario` también hereda campos de `AbstractUser`.

## 7. Parámetros de los campos

| Parámetro | Descripción |
|---|---|
| `max_length` | Longitud máxima del texto |
| `blank` | Permite dejar el campo vacío en formularios y validación |
| `null` | Permite almacenar `NULL` en la base de datos |
| `default` | Establece un valor predeterminado |
| `auto_now_add` | Establece automáticamente la fecha y hora de creación |
| `on_delete` | Define qué ocurre al eliminar el objeto relacionado |
| `related_name` | Define el nombre de acceso inverso a la relación |
| `max_digits` | Número máximo de dígitos de un `DecimalField` |
| `decimal_places` | Número de cifras decimales de un `DecimalField` |
| `choices` | Define las opciones permitidas para un campo |
| `through` | Especifica el modelo intermedio de una relación muchos a muchos |

**Diferencia entre `blank` y `null`:** `blank` afecta a la validación; `null` afecta al almacenamiento en la base de datos.

## 8. Diagrama entidad-relación

El diagrama entidad-relación debe representar los 16 modelos y las relaciones descritas en este documento.

Para evitar que las imágenes dependan de enlaces temporales, se recomienda guardar el diagrama en el repositorio, por ejemplo en `docs/diagrama-er.png`, y mostrarlo así:

```markdown
![Diagrama entidad-relación de GameLoop](docs/diagrama-er.png)
```

## 9. Generación de datos de prueba

El proyecto dispone de un comando personalizado en:

`core/management/commands/seed.py`

Se ejecuta con:

```bash
python3 manage.py seed
```

Este comando permite generar datos de prueba para comprobar los modelos y sus relaciones. El número exacto de registros creados por modelo debe corresponder a la implementación de `seed.py`.

## 10. Instalación y ejecución

Desde la carpeta raíz del proyecto:

### Crear y activar el entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar dependencias

```bash
python3 -m pip install -r requirements.txt
```

### Aplicar migraciones

```bash
python3 manage.py migrate
```

Si todavía no existen migraciones para los modelos, se pueden generar con:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Iniciar el servidor

```bash
python3 manage.py runserver
```

Por defecto, Django estará disponible en:

`http://127.0.0.1:8000/`

## 11. Copias de seguridad y fixtures

Django permite exportar e importar datos mediante fixtures.

### 11.1. Exportar los datos

```bash
python3 manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --exclude=contenttypes \
  --exclude=auth.permission \
  --exclude=sessions \
  --indent 2 \
  -o backup.json
```

### 11.2. Importar los datos

```bash
python3 manage.py loaddata backup.json
```

Para restaurar una copia, deben estar aplicadas las migraciones y la base de datos debe ser compatible. Es recomendable comprobar que el fixture puede restaurarse correctamente.

## 12. Control de versiones

Git permite mantener el historial de cambios del proyecto. El repositorio utiliza las ramas de trabajo `Configuracion_inicial`, `Modelos`, `Backups` y `main`.

El archivo `.gitignore` debería excluir el entorno virtual (`.venv/` o `venv/`), `__pycache__/`, los archivos compilados de Python y las configuraciones locales sensibles. Deben mantenerse en el repositorio los archivos necesarios para la entrega, como `requirements.txt`, las migraciones y el fixture cuando corresponda.

## 12. Conclusión

GameLoop permite aplicar conceptos de desarrollo web con Django y Python 3 mediante modelos, relaciones entre entidades, datos de prueba y copias de seguridad. La documentación describe la estructura actual del proyecto y señala las comprobaciones necesarias para verificar el cumplimiento completo del enunciado.
