 
# GameLoop — Documentación del proyecto

## 1. Descripción del proyecto

**GameLoop** es una aplicación web desarrollada con Django que permite crear una comunidad de usuarios relacionada con los videojuegos. La aplicación incluye funcionalidades para gestionar perfiles, amistades, grupos, juegos, noticias, comentarios, reacciones, chats, mensajes y notificaciones.

El objetivo del proyecto es poner en práctica el desarrollo de aplicaciones web con Django, el diseño de modelos, las relaciones entre entidades, la generación de datos de prueba y la gestión de copias de seguridad de la base de datos.

## 2. Tecnologías utilizadas

- **Python 3:** lenguaje de programación utilizado para desarrollar la aplicación.
- **Django:** framework web empleado para construir la aplicación.
- **SQLite:** base de datos utilizada por defecto en proyectos Django, salvo que la configuración indique otra.
- **Faker:** biblioteca utilizada para generar datos ficticios de prueba, si está instalada y configurada en el proyecto.
- **Git y GitHub:** herramientas para el control de versiones y el almacenamiento del código fuente.

## 3. Repositorio de GitHub

El código fuente del proyecto se encuentra en el siguiente repositorio:

[Proyecto_2_DAW — GitHub](https://github.com/CLASEJMFL/Proyecto_2_DAW)

Autores:

- Alejandro Fernández Linares
- José Manuel Fernández Linares

## 4. Estructura del proyecto

El proyecto está organizado siguiendo la estructura habitual de Django.

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

Descripción de los elementos principales:

- `manage.py`: permite ejecutar comandos de administración de Django.
- `requirements.txt`: contiene las dependencias necesarias para ejecutar el proyecto.
- `backup.json`: archivo destinado a almacenar datos exportados de la base de datos.
- `.gitignore`: indica qué archivos y carpetas no deben incluirse en el repositorio.
- `core/models.py`: contiene los modelos y las relaciones de la aplicación.
- `core/admin.py`: permite configurar la administración de los modelos desde Django Admin.
- `core/management/commands/seed.py`: contiene el comando personalizado para generar datos de prueba.

## 5. Modelos de la aplicación

La aplicación contiene 16 modelos principales, definidos en `core/models.py`.

### 5.1. Usuario

Representa a los usuarios registrados en la aplicación.

Hereda de `AbstractUser`, por lo que aprovecha el sistema de autenticación de Django y sus campos habituales, como el nombre de usuario, el correo electrónico y la contraseña.

### 5.2. PerfilUsuario

Almacena información adicional del perfil de cada usuario, separada de los datos de autenticación.

Mantiene una relación uno a uno con `Usuario`.

### 5.3. ConfiguracionUsuario

Almacena las preferencias y opciones de configuración de cada usuario.

Mantiene una relación uno a uno con `Usuario`.

### 5.4. EstadisticasUsuario

Permite guardar estadísticas asociadas a cada usuario.

Mantiene una relación uno a uno con `Usuario`.

### 5.5. Amistad

Representa las relaciones de amistad entre usuarios mediante referencias a los usuarios implicados.

### 5.6. Grupo

Representa grupos o comunidades dentro de GameLoop. Permite relacionar usuarios con grupos y asociar juegos a estos.

### 5.7. Pertenencia

Representa la pertenencia de un usuario a un grupo. Actúa como modelo intermedio entre `Usuario` y `Grupo`.

### 5.8. Juego

Representa los videojuegos registrados en la aplicación.

### 5.9. Noticia

Almacena noticias relacionadas con la comunidad y los videojuegos.

### 5.10. Comentario

Permite registrar comentarios asociados al contenido correspondiente y a los usuarios que los publican.

### 5.11. Reaccion

Representa las reacciones de los usuarios ante el contenido de la aplicación.

### 5.12. UsuarioJuego

Relaciona a los usuarios con los videojuegos y permite almacenar información adicional sobre esa relación.

### 5.13. Chat

Representa las conversaciones entre usuarios.

### 5.14. ParticipanteChat

Es el modelo intermedio que relaciona usuarios con chats.

### 5.15. Mensaje

Almacena los mensajes enviados en las conversaciones.

### 5.16. Notificacion

Representa las notificaciones generadas para los usuarios.

## 6. Relaciones entre los modelos

En Django, las relaciones se definen mediante campos como `ForeignKey`, `OneToOneField` y `ManyToManyField`.

### 6.1. Relaciones uno a uno

Se utilizan para asociar un único registro con otro.

En el proyecto existen estas relaciones:

- `Usuario` — `PerfilUsuario`.
- `Usuario` — `ConfiguracionUsuario`.
- `Usuario` — `EstadisticasUsuario`.

Estas relaciones permiten separar la información adicional del usuario en diferentes modelos.

### 6.2. Relaciones uno a muchos

Se implementan mediante `ForeignKey`.

Un registro del modelo relacionado puede estar asociado a varios registros del modelo que contiene la clave foránea. Por ejemplo, un chat puede tener varios mensajes, y un usuario puede estar asociado a diferentes registros de actividad, comentarios o notificaciones, según la definición de cada modelo.

### 6.3. Relaciones muchos a muchos

Se implementan mediante `ManyToManyField`.

En el proyecto destacan:

- **Grupo y Usuario:** la relación se gestiona mediante el modelo intermedio `Pertenencia`.
- **Chat y Usuario:** la relación se gestiona mediante el modelo intermedio `ParticipanteChat`.
- **Grupo y Juego:** los grupos pueden relacionarse con varios juegos mediante una relación muchos a muchos.

Los modelos intermedios permiten representar la relación entre las entidades y almacenar información adicional sobre ella cuando el modelo está diseñado para ello.

## 7. Tipos de campos utilizados

Django proporciona distintos tipos de campos para definir los atributos de los modelos.

| Tipo de campo | Utilidad |
|---|---|
| `CharField` | Almacena cadenas de texto de longitud limitada. |
| `TextField` | Almacena textos largos. |
| `BooleanField` | Almacena valores verdadero o falso. |
| `PositiveIntegerField` | Almacena números enteros no negativos. |
| `PositiveSmallIntegerField` | Almacena números enteros pequeños no negativos. |
| `FloatField` | Almacena números decimales de coma flotante. |
| `DecimalField` | Almacena valores decimales con precisión definida. |
| `DateField` | Almacena fechas. |
| `DateTimeField` | Almacena fechas y horas. |
| `URLField` | Almacena direcciones URL. |

La elección del campo depende del tipo de información que se necesita almacenar.

## 8. Parámetros de los campos

Los campos de Django pueden incluir parámetros para controlar su comportamiento.

| Parámetro | Descripción |
|---|---|
| `max_length` | Establece la longitud máxima de un campo de texto. |
| `blank` | Indica si un campo puede dejarse vacío en la validación de formularios. |
| `null` | Indica si la base de datos puede almacenar `NULL` en ese campo. |
| `default` | Define el valor predeterminado del campo. |
| `auto_now_add` | Asigna automáticamente la fecha y hora de creación. |
| `on_delete` | Determina qué sucede cuando se elimina el objeto relacionado. |
| `related_name` | Define el nombre utilizado para acceder a la relación desde el modelo relacionado. |
| `max_digits` | Establece el número máximo de dígitos de un `DecimalField`. |
| `decimal_places` | Establece cuántas cifras decimales puede almacenar un `DecimalField`. |
| `choices` | Define un conjunto de opciones permitidas para un campo. |
| `through` | Indica el modelo intermedio utilizado en una relación muchos a muchos. |

Es importante diferenciar `blank` y `null`: el primero afecta a la validación, mientras que el segundo afecta al almacenamiento en la base de datos.

## 9. Diagrama de entidades y relaciones

El siguiente diagrama representa de forma general las principales entidades de GameLoop y sus relaciones.

<img width="803" height="520" alt="image" src="https://github.com/user-attachments/assets/f5cd8065-c805-4d33-91ed-821d6e92098d" />

<img width="907" height="566" alt="image" src="https://github.com/user-attachments/assets/7df9f2e7-4d84-448a-8fec-80c99e71ff72" />



## 10. Generación de datos de prueba

El proyecto incluye un comando personalizado en:

```text
core/management/commands/seed.py
```

Este archivo permite crear datos de prueba para facilitar las comprobaciones de la aplicación durante el desarrollo.

Si el comando está registrado correctamente como comando de administración de Django, se puede ejecutar con Python 3:

```bash
python3 manage.py seed
```

La generación de datos de prueba facilita comprobar las relaciones entre modelos y probar las funcionalidades sin tener que introducir manualmente todos los registros.

Si se utiliza Faker, esta biblioteca permite generar datos ficticios, como nombres, direcciones de correo y otros valores de prueba.

## 11. Instalación y ejecución con Python 3

### 11.1. Requisitos previos

Es necesario disponer de Python 3 y de `pip3`. Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

### 11.2. Crear un entorno virtual

Desde la carpeta raíz del proyecto, ejecutar:

```bash
python3 -m venv venv
```

Activación en Linux o macOS:

```bash
source venv/bin/activate
```

Activación en Windows:

```powershell
venv\Scripts\activate
```

### 11.3. Instalar las dependencias

Con el entorno virtual activado:

```bash
python3 -m pip install -r requirements.txt
```

### 11.4. Aplicar las migraciones

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Si las migraciones ya están incluidas en el proyecto, normalmente bastará con ejecutar `migrate`.

### 11.5. Ejecutar el servidor

```bash
python3 manage.py runserver
```

A continuación, se puede acceder a la aplicación desde el navegador en:

```text
http://127.0.0.1:8000/
```

## 12. Copias de seguridad y fixtures

Django permite exportar e importar datos mediante el sistema de serialización. Los archivos generados de esta manera se conocen como fixtures.

### 12.1. Exportar datos

Para crear una copia de los datos de la aplicación en `backup.json`, se puede ejecutar:

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

Este comando exporta los datos de la base de datos a un archivo JSON, excluyendo los modelos indicados.

### 12.2. Importar datos

Para cargar los datos almacenados en el archivo:

```bash
python3 manage.py loaddata backup.json
```

La importación debe realizarse con una base de datos compatible y con las tablas y migraciones preparadas. Conviene probar las copias de seguridad antes de depender de ellas como único mecanismo de recuperación.

## 13. Archivo `.gitignore`

El archivo `.gitignore` permite evitar que determinados archivos locales se añadan al repositorio.

Es habitual excluir:

- El entorno virtual (`venv/`).
- Los archivos compilados de Python (`__pycache__/` y `*.py[cod]`).
- Los archivos de configuración local que contengan información sensible.
- Las bases de datos locales, si no deben versionarse.
- Los archivos temporales generados durante el desarrollo.

La configuración definitiva debe respetar los archivos que el proyecto necesita mantener en Git, como `requirements.txt`, las migraciones y los fixtures que se quieran entregar.



## 14. Conclusión

GameLoop permite aplicar los conceptos fundamentales del desarrollo de aplicaciones web con Django y Python 3. La estructura de modelos permite representar usuarios, perfiles, grupos, juegos, noticias, conversaciones y notificaciones, mientras que las relaciones facilitan conectar la información almacenada.

Además, el uso de comandos personalizados para generar datos de prueba y de fixtures para exportar e importar información facilita el desarrollo, la comprobación de funcionalidades y la preparación de copias de seguridad.
