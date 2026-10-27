# GameLoop — Documentación del proyecto 🎮

## 1. Descripción del proyecto

**GameLoop** es una aplicación web desarrollada con Django que permite crear una comunidad de usuarios relacionada con los videojuegos. Incluye perfiles, amistades, grupos, juegos, noticias, comentarios, reacciones, chats, mensajes y notificaciones.

El objetivo es poner en práctica el diseño de modelos, las relaciones entre entidades, la generación de datos de prueba y las copias de seguridad de una aplicación web.

## 2. Tecnologías utilizadas

- **Python 3:** lenguaje de programación.
- **Django:** framework para el desarrollo web.
- **SQLite:** base de datos si se mantiene la configuración predeterminada de Django.
- **Faker:** biblioteca para generar datos ficticios de prueba.
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
- `backup.json`: archivo de copia de seguridad de los datos, si está generado.
- `.gitignore`: excluye archivos locales que no deben incluirse en Git.
- `core/models.py`: contiene los modelos y sus relaciones.
- `core/admin.py`: configura la administración de los modelos.
- `core/management/commands/seed.py`: contiene el comando personalizado para generar datos de prueba.

## 4. Modelos de la aplicación

El proyecto cuenta con 16 modelos declarados en `core/models.py`.

### 4.1. Usuario

Hereda de `AbstractUser`, que proporciona campos de autenticación y gestión de cuentas, como `username`, `first_name`, `last_name`, `email` y `password`.

| Campo | Tipo | Parámetros |
|---|---|---|
| `foto_perfil` | `URLField` | `blank=True` |
| `biografia` | `TextField` | `blank=True` |
| `fecha_registro` | `DateTimeField` | `auto_now_add=True` |

Representa a los usuarios registrados en GameLoop.

### 4.2. PerfilUsuario

Almacena información adicional del perfil de cada usuario.

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

Almacena estadísticas relacionadas con la actividad del usuario.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `OneToOneField` | `on_delete=CASCADE`, `related_name="estadisticas"` |
| `juegos_favoritos` | `PositiveIntegerField` | `default=0` |
| `horas_totales` | `FloatField` | `default=0` |
| `nivel` | `PositiveSmallIntegerField` | `default=1` |
| `puntuacion_media` | `DecimalField` | `max_digits=4`, `decimal_places=2`, `default=0` |

### 4.5. Amistad

Representa las solicitudes y relaciones de amistad entre usuarios.

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

La relación con los usuarios utiliza el modelo intermedio `Pertenencia`, que almacena información adicional sobre la pertenencia. La relación con los videojuegos utiliza una tabla intermedia generada automáticamente por Django.

### 4.7. Pertenencia

Representa la pertenencia de un usuario a un grupo y almacena información adicional de esa relación.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `grupo` | `ForeignKey` | `on_delete=CASCADE` |
| `rol` | `CharField` | `max_length=30`, `default="miembro"` |
| `fecha_union` | `DateTimeField` | `auto_now_add=True` |

Es el modelo intermedio de la relación muchos a muchos entre usuarios y grupos.

### 4.8. Juego

Representa los videojuegos registrados en la plataforma.

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
| `contenido` | `TextField` | Sin parámetros adicionales declarados |
| `fecha_publicacion` | `DateTimeField` | `auto_now_add=True` |
| `autor` | `ForeignKey` | `on_delete=CASCADE` |
| `grupo` | `ForeignKey` | `on_delete=CASCADE`, `null=True`, `blank=True` |
| `juego` | `ForeignKey` | `on_delete=CASCADE` |

El grupo asociado a una noticia es opcional. Cada noticia tiene un autor y está relacionada con un videojuego.

### 4.10. Comentario

Representa comentarios publicados en noticias.

| Campo | Tipo | Parámetros |
|---|---|---|
| `contenido` | `TextField` | Sin parámetros adicionales declarados |
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

Almacena la asociación entre usuarios y videojuegos, junto con datos de su actividad.

| Campo | Tipo | Parámetros |
|---|---|---|
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `juego` | `ForeignKey` | `on_delete=CASCADE` |
| `horas_jugadas` | `FloatField` | `default=0` |
| `favorito` | `BooleanField` | `default=False` |
| `fecha_inicio` | `DateField` | `null=True`, `blank=True` |

Este modelo dispone de dos claves foráneas y atributos adicionales. Para que Django utilice formalmente `UsuarioJuego` como tabla intermedia de una relación `ManyToManyField`, debe declararse explícitamente el campo correspondiente con `through="UsuarioJuego"`.

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

Es el modelo intermedio que relaciona usuarios y chats.

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
| `contenido` | `TextField` | Sin parámetros adicionales declarados |
| `fecha_envio` | `DateTimeField` | `auto_now_add=True` |
| `autor` | `ForeignKey` | `on_delete=CASCADE` |
| `chat` | `ForeignKey` | `on_delete=CASCADE` |

### 4.16. Notificacion

Representa las notificaciones dirigidas a los usuarios.

| Campo | Tipo | Parámetros |
|---|---|---|
| `tipo` | `CharField` | `max_length=20`, `choices=TIPO_CHOICES` |
| `mensaje` | `TextField` | Sin parámetros adicionales declarados |
| `fecha` | `DateTimeField` | `auto_now_add=True` |
| `usuario` | `ForeignKey` | `on_delete=CASCADE` |
| `leida` | `BooleanField` | `default=False` |

Las opciones de `tipo` son `amistad`, `comentario`, `mensaje` y `grupo`.

## 5. Relaciones entre modelos

### 5.1. Relaciones uno a uno (OneToOne)

Se utiliza `OneToOneField` para establecer una relación exclusiva entre dos registros.

| Modelo principal | Modelo relacionado | Campo de relación |
|---|---|---|
| `Usuario` | `PerfilUsuario` | `PerfilUsuario.usuario` |
| `Usuario` | `ConfiguracionUsuario` | `ConfiguracionUsuario.usuario` |
| `Usuario` | `EstadisticasUsuario` | `EstadisticasUsuario.usuario` |

Cada perfil, configuración y registro de estadísticas pertenece a un único usuario. Un usuario puede tener como máximo un registro relacionado de cada uno de estos modelos.

### 5.2. Relaciones uno a muchos (ForeignKey)

Se implementan mediante `ForeignKey`. Desde la perspectiva del modelo que contiene la clave foránea, son relaciones muchos a uno.

| Modelo que contiene la clave foránea | Modelo relacionado | Campo |
|---|---|---|
| `Amistad` | `Usuario` | `usuario_origen` |
| `Amistad` | `Usuario` | `usuario_destino` |
| `Pertenencia` | `Usuario` | `usuario` |
| `Pertenencia` | `Grupo` | `grupo` |
| `Noticia` | `Usuario` | `autor` |
| `Noticia` | `Grupo` | `grupo` |
| `Noticia` | `Juego` | `juego` |
| `Comentario` | `Usuario` | `usuario` |
| `Comentario` | `Noticia` | `noticia` |
| `Reaccion` | `Usuario` | `usuario` |
| `Reaccion` | `Noticia` | `noticia` |
| `UsuarioJuego` | `Usuario` | `usuario` |
| `UsuarioJuego` | `Juego` | `juego` |
| `ParticipanteChat` | `Usuario` | `usuario` |
| `ParticipanteChat` | `Chat` | `chat` |
| `Mensaje` | `Usuario` | `autor` |
| `Mensaje` | `Chat` | `chat` |
| `Notificacion` | `Usuario` | `usuario` |

El campo `Noticia.grupo` permite valores nulos, por lo que una noticia puede no estar asociada a ningún grupo.

### 5.3. Relaciones muchos a muchos (ManyToMany)

| Modelo principal | Modelo relacionado | Implementación | Atributos adicionales |
|---|---|---|---|
| `Grupo` | `Usuario` | `ManyToManyField` mediante `Pertenencia` | `rol`, `fecha_union` |
| `Chat` | `Usuario` | `ManyToManyField` mediante `ParticipanteChat` | `fecha_union`, `rol` |
| `Grupo` | `Juego` | `ManyToManyField` con tabla intermedia automática | No declarados |

Los modelos `Pertenencia` y `ParticipanteChat` permiten almacenar datos adicionales de las relaciones.

**Nota sobre UsuarioJuego:** en el código documentado, `UsuarioJuego` tiene dos `ForeignKey`, pero no consta un `ManyToManyField` que lo utilice mediante `through`. Por ello, no se contabiliza como una relación muchos a muchos declarada formalmente hasta que se incorpore ese campo.

## 6. Tipos de campos utilizados

Los modelos emplean los siguientes tipos de campos de Django:

| Tipo de campo | Descripción |
|---|---|
| `CharField` | Texto de longitud limitada. |
| `TextField` | Texto largo. |
| `BooleanField` | Valor verdadero o falso. |
| `PositiveIntegerField` | Entero no negativo. |
| `PositiveSmallIntegerField` | Entero pequeño no negativo. |
| `FloatField` | Número de coma flotante. |
| `DecimalField` | Número decimal con precisión definida. |
| `DateField` | Fecha. |
| `DateTimeField` | Fecha y hora. |
| `URLField` | Dirección URL. |
| `OneToOneField` | Relación uno a uno. |
| `ForeignKey` | Relación muchos a uno. |
| `ManyToManyField` | Relación muchos a muchos. |

Los tres últimos son campos relacionales; los diez primeros son tipos de campos no relacionales.

## 7. Parámetros de los campos

| Parámetro | Descripción | Ejemplo en el proyecto |
|---|---|---|
| `max_length` | Longitud máxima de un campo de texto. | `max_length=100` |
| `blank` | Permite dejar vacío un campo durante la validación. | `blank=True` |
| `null` | Permite almacenar `NULL` en la base de datos. | `null=True` |
| `default` | Establece un valor predeterminado. | `default=False` |
| `auto_now_add` | Establece automáticamente la fecha y hora al crear el registro. | `auto_now_add=True` |
| `on_delete` | Define el comportamiento al eliminar el objeto relacionado. | `on_delete=CASCADE` |
| `related_name` | Define el nombre de acceso inverso a la relación. | `related_name="comentarios"` |
| `max_digits` | Número máximo de dígitos de un `DecimalField`. | `max_digits=4` |
| `decimal_places` | Número de cifras decimales de un `DecimalField`. | `decimal_places=2` |
| `choices` | Define las opciones disponibles para un campo. | `choices=TIPO_CHOICES` |
| `through` | Especifica el modelo intermedio de una relación muchos a muchos. | `through="Pertenencia"` |

**Diferencia entre `blank` y `null`:** `blank` afecta a la validación del campo; `null` afecta al almacenamiento en la base de datos.

## 8. Diagrama entidad-relación

<img width="1085" height="789" alt="modelo entidad relacion" src="https://github.com/user-attachments/assets/b4fe0312-9f53-4b35-85ca-c85609affbd4" />
<img width="1536" height="1024" alt="modelo relacional" src="https://github.com/user-attachments/assets/e3abb246-dce2-4e7c-b1a7-fe00ea999493" />


## 9. Generación de datos de prueba

El proyecto dispone de un comando personalizado ubicado en:

`core/management/commands/seed.py`

Para ejecutarlo:

```bash
python3 manage.py seed
```

El comando permite generar datos de prueba para comprobar los modelos y sus relaciones.

Si el requisito de la práctica es crear diez registros aleatorios por cada modelo, debe verificarse que la implementación de `seed.py` genere diez registros de cada modelo y respete las dependencias entre entidades.

## 10. Instalación y ejecución

Los siguientes comandos se ejecutan desde la carpeta raíz del proyecto.

### 10.1. Crear y activar el entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 10.2. Instalar dependencias

```bash
python3 -m pip install -r requirements.txt
```

### 10.3. Crear y aplicar migraciones

Si todavía no existen migraciones para los modelos:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Si las migraciones ya existen en el repositorio:

```bash
python3 manage.py migrate
```

### 10.4. Crear un superusuario

```bash
python3 manage.py createsuperuser
```

### 10.5. Iniciar el servidor

```bash
python3 manage.py runserver
```

Por defecto, el servidor de desarrollo estará disponible en:

`http://127.0.0.1:8000/`

## 11. Copias de seguridad y fixtures

Django permite exportar e importar datos mediante fixtures.

### 11.1. Exportar los datos

Para generar una copia de seguridad en `backup.json`:

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

Para cargar los datos del archivo:

```bash
python3 manage.py loaddata backup.json
```

Antes de restaurar una copia, deben estar aplicadas las migraciones correspondientes. Es recomendable comprobar que el fixture puede importarse correctamente en una base de datos compatible.

## 12. Control de versiones

Git permite registrar los cambios del proyecto y mantener diferentes ramas de trabajo.

Las ramas utilizadas son:

- `Configuracion_inicial`: configuración inicial del proyecto.
- `Modelos`: desarrollo de los modelos y sus relaciones.
- `Backups`: trabajo relacionado con las copias de seguridad.
- `main`: rama principal del proyecto.

El archivo `.gitignore` debe excluir el entorno virtual (`.venv/` o `venv/`), `__pycache__/`, los archivos compilados de Python y las configuraciones locales sensibles.

Deben mantenerse en el repositorio los archivos necesarios para ejecutar y evaluar el proyecto, como `requirements.txt`, las migraciones y el fixture cuando corresponda.

## 13. Conclusión

GameLoop aplica conceptos de desarrollo web con Django y Python mediante modelos, relaciones entre entidades, datos de prueba y copias de seguridad.

Este documento describe los modelos, sus campos, los parámetros principales y las relaciones declaradas en el proyecto. La implementación del código y las comprobaciones finales deben mantenerse sincronizadas con esta documentación.
