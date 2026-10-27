Grupo Alejandro Fernández Linares y José Manuel Fernández Linares
# GameLoop — Modelos y base de datos

## 1. Modelos de la aplicación

<img width="662" height="425" alt="image" src="https://github.com/user-attachments/assets/ef4d311f-f031-44ef-859e-5e9740669418" />


### 1.1. Perfil
Almacena la información personal y pública de cada usuario.

- `usuario`: relación uno a uno con el usuario de Django.
- `biografia`: descripción personal del usuario.
- `foto`: imagen del perfil.
- `fecha_nacimiento`: fecha de nacimiento.
- `web`: página web personal.

### 1.2. Preferencias
Almacena las preferencias de configuración de cada usuario.

- `usuario`: relación uno a uno con el usuario de Django.
- `tema`: tema visual seleccionado.
- `idioma`: idioma de la aplicación.
- `recibir_emails`: indica si recibe correos electrónicos.
- `mostrar_perfil`: indica si el perfil es visible.

### 1.3. Estadisticas
Guarda las estadísticas de actividad de cada usuario.

- `usuario`: relación uno a uno con el usuario de Django.
- `puntos`: puntos acumulados.
- `nivel`: nivel del usuario.
- `tiempo_jugado`: tiempo total jugado.
- `ultima_actividad`: fecha y hora de la última actividad.

### 1.4. Juego
Representa los videojuegos disponibles en la aplicación.

- `nombre`: nombre del videojuego.
- `descripcion`: información sobre el juego.
- `genero`: género del videojuego.
- `fecha_lanzamiento`: fecha de lanzamiento.
- `precio`: precio del videojuego.
- `activo`: indica si el juego está disponible.
- `usuarios`: relación muchos a muchos con usuarios mediante `UsuarioJuego`.

### 1.5. Grupo
Representa grupos de usuarios que comparten intereses relacionados con videojuegos.

- `nombre`: nombre del grupo.
- `descripcion`: descripción del grupo.
- `fecha_creacion`: fecha de creación.
- `publico`: indica si el grupo es público.
- `max_miembros`: número máximo de miembros.
- `miembros`: relación muchos a muchos con usuarios mediante `PertenenciaGrupo`.

### 1.6. PertenenciaGrupo
Relaciona usuarios con grupos y almacena información adicional sobre su pertenencia.

- `usuario`: usuario que pertenece al grupo.
- `grupo`: grupo correspondiente.
- `rol`: función del usuario dentro del grupo.
- `fecha_union`: fecha de incorporación.
- `activo`: indica si la pertenencia sigue activa.

### 1.7. Noticia
Almacena noticias relacionadas con videojuegos.

- `titulo`: título de la noticia.
- `contenido`: texto de la noticia.
- `fecha_publicacion`: fecha de publicación.
- `publicada`: indica si la noticia está publicada.
- `visitas`: número de visitas.
- `autor`: usuario que ha creado la noticia.
- `juego`: videojuego relacionado con la noticia.

### 1.8. Comentario
Almacena los comentarios realizados en las noticias.

- `contenido`: texto del comentario.
- `fecha`: fecha de creación.
- `editado`: indica si se ha modificado.
- `puntuacion`: puntuación del comentario.
- `usuario`: usuario que realiza el comentario.
- `noticia`: noticia comentada.

### 1.9. Reaccion
Almacena las reacciones de los usuarios a las noticias.

- `tipo`: tipo de reacción.
- `fecha`: fecha de la reacción.
- `activa`: indica si la reacción está activa.
- `intensidad`: intensidad de la reacción.
- `usuario`: usuario que reacciona.
- `noticia`: noticia que recibe la reacción.

### 1.10. UsuarioJuego
Relaciona usuarios con videojuegos y guarda información sobre su actividad.

- `usuario`: usuario relacionado.
- `juego`: videojuego registrado.
- `horas_jugadas`: horas dedicadas al juego.
- `favorito`: indica si es uno de los juegos favoritos.
- `fecha_inicio`: fecha en que comenzó a jugar.
- `plataforma`: plataforma utilizada.

### 1.11. Amistad
Gestiona las solicitudes y relaciones de amistad entre usuarios.

- `usuario`: usuario que envía la solicitud.
- `amigo`: usuario que la recibe.
- `estado`: estado de la solicitud.
- `fecha_solicitud`: fecha de envío.
- `fecha_aceptacion`: fecha de aceptación.
- `nota`: mensaje opcional.

### 1.12. Chat
Representa una conversación entre usuarios.

- `nombre`: nombre de la conversación.
- `tipo`: tipo de chat.
- `fecha_creacion`: fecha de creación.
- `activo`: indica si el chat está activo.
- `descripcion`: descripción de la conversación.
- `participantes`: relación muchos a muchos con usuarios mediante `ParticipanteChat`.

### 1.13. ParticipanteChat
Relaciona usuarios con conversaciones y almacena información sobre su participación.

- `usuario`: usuario participante.
- `chat`: conversación correspondiente.
- `fecha_union`: fecha de incorporación.
- `rol`: función del usuario en el chat.
- `silenciado`: indica si el chat está silenciado para ese usuario.

### 1.14. Mensaje
Almacena los mensajes enviados en los chats.

- `contenido`: texto del mensaje.
- `fecha_envio`: fecha de envío.
- `editado`: indica si se ha editado.
- `tipo`: tipo de mensaje.
- `leido`: indica si se ha leído.
- `autor`: usuario que envía el mensaje.
- `chat`: conversación a la que pertenece.

### 1.15. Notificacion
Almacena las notificaciones recibidas por los usuarios.

- `tipo`: tipo de notificación.
- `mensaje`: contenido de la notificación.
- `fecha`: fecha de creación.
- `leida`: indica si se ha leído.
- `prioridad`: nivel de prioridad.
- `usuario`: usuario que recibe la notificación.

### 1.16. PublicacionRedSocial
Registra las publicaciones de noticias destinadas a redes sociales externas.

- `noticia`: noticia que se quiere publicar.
- `red_social`: red social de destino.
- `fecha_publicacion`: fecha del registro de publicación.
- `estado`: estado del envío.
- `url_publicacion`: enlace a la publicación externa.
- `mensaje_error`: descripción de un posible error.

## 2. Parámetros y tipos de campos utilizados

### Tipos de campos

- `CharField`: almacena texto corto.
- `TextField`: almacena texto largo.
- `BooleanField`: almacena valores verdaderos o falsos.
- `IntegerField`: almacena números enteros.
- `PositiveIntegerField`: almacena números enteros no negativos.
- `PositiveSmallIntegerField`: almacena números enteros pequeños no negativos.
- `FloatField`: almacena números decimales de coma flotante.
- `DecimalField`: almacena números decimales de precisión fija.
- `DateField`: almacena fechas.
- `DateTimeField`: almacena fechas y horas.
- `URLField`: almacena direcciones web.
- `ImageField`: almacena la ruta de una imagen.
- `OneToOneField`: establece una relación uno a uno.
- `ForeignKey`: establece una relación muchos a uno.
- `ManyToManyField`: establece una relación muchos a muchos.

### Parámetros

- `max_length`: establece la longitud máxima de un texto.
- `default`: establece un valor predeterminado.
- `blank=True`: permite dejar el campo vacío en formularios y validaciones.
- `null=True`: permite almacenar un valor nulo en la base de datos.
- `unique=True`: impide que se repita un valor.
- `auto_now_add=True`: establece automáticamente la fecha y hora de creación.
- `upload_to`: indica la carpeta donde se guardan las imágenes.
- `max_digits`: establece el número máximo de dígitos de un campo decimal.
- `decimal_places`: establece el número de cifras decimales.
- `on_delete`: define qué ocurre cuando se elimina el objeto relacionado.
- `CASCADE`: elimina los registros relacionados cuando se elimina el objeto principal.
- `SET_NULL`: establece la relación como nula cuando se elimina el objeto relacionado.
- `related_name`: define el nombre utilizado para acceder a una relación inversa.
- `through`: indica el modelo intermedio de una relación muchos a muchos.
- `constraints`: define restricciones sobre los registros.
- `fields`: indica los campos a los que se aplica una restricción.
- `name`: establece el nombre de una restricción.

## 3. Esquema del modelo entidad-relación


El esquema entidad-relación representa las tablas de la base de datos, sus atributos y las relaciones entre ellas.

Las relaciones principales son:

- `User` — `Perfil`: uno a uno.
- `User` — `Preferencias`: uno a uno.
- `User` — `Estadisticas`: uno a uno.
- `User` — `Noticia`: uno a muchos.
- `Noticia` — `Comentario`: uno a muchos.
- `Chat` — `Mensaje`: uno a muchos.
- `User` — `Juego`: muchos a muchos mediante `UsuarioJuego`.
- `User` — `Grupo`: muchos a muchos mediante `PertenenciaGrupo`.
- `User` — `Chat`: muchos a muchos mediante `ParticipanteChat`.
- `Noticia` — `PublicacionRedSocial`: uno a muchos.

El diagrama debe incluir todos los modelos, sus atributos, las claves primarias, las claves foráneas y las cardinalidades de las relaciones.

**Diagrama entidad-relación:**
<img width="882" height="557" alt="image" src="https://github.com/user-attachments/assets/bb5f4a23-c022-4d79-9ecc-2fd75cf929c9" />


