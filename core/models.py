from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    foto_perfil = models.URLField(blank=True)
    biografia = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil"
    )
    nombre_visible = models.CharField(max_length=100, blank=True)
    biografia = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    web = models.URLField(blank=True)

    def __str__(self):
        return self.usuario.username


class ConfiguracionUsuario(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="configuracion"
    )
    tema_oscuro = models.BooleanField(default=False)
    notificaciones_activadas = models.BooleanField(default=True)
    idioma = models.CharField(max_length=10, default="es")

    def __str__(self):
        return self.usuario.username


class EstadisticasUsuario(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="estadisticas"
    )
    juegos_favoritos = models.PositiveIntegerField(default=0)
    horas_totales = models.FloatField(default=0)
    nivel = models.PositiveSmallIntegerField(default=1)
    puntuacion_media = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.usuario.username


class Amistad(models.Model):
    usuario_origen = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="amistades_enviadas"
    )
    usuario_destino = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="amistades_recibidas"
    )
    estado = models.CharField(max_length=20, default="pendiente")
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_aceptacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario_origen} -> {self.usuario_destino}"


class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.URLField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    usuarios = models.ManyToManyField(
        Usuario,
        through="Pertenencia",
        related_name="grupos"
    )

    juegos = models.ManyToManyField(
        "Juego",
        blank=True,
        related_name="grupos"
    )

    def __str__(self):
        return self.nombre


class Pertenencia(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE
    )
    rol = models.CharField(max_length=30, default="miembro")
    fecha_union = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.grupo}"


class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    genero = models.CharField(max_length=50)
    imagen = models.URLField(blank=True)
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    plataformas = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre


class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
    noticia = models.ForeignKey(
        Noticia,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )

    def __str__(self):
        return self.contenido[:50]


class Reaccion(models.Model):
    TIPO_CHOICES = [
        ("me_gusta", "Me gusta"),
        ("no_me_gusta", "No me gusta"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
    noticia = models.ForeignKey(
        Noticia,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.usuario}: {self.tipo}"


class UsuarioJuego(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE
    )
    horas_jugadas = models.FloatField(default=0)
    favorito = models.BooleanField(default=False)
    fecha_inicio = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.juego}"


class Chat(models.Model):
    TIPO_CHOICES = [
        ("privado", "Privado"),
        ("grupal", "Grupal"),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=100, blank=True)

    participantes = models.ManyToManyField(
        Usuario,
        through="ParticipanteChat",
        related_name="chats"
    )

    def __str__(self):
        return self.nombre or f"Chat {self.pk}"


class ParticipanteChat(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE
    )
    fecha_union = models.DateTimeField(auto_now_add=True)
    rol = models.CharField(max_length=30, default="miembro")

    def __str__(self):
        return f"{self.usuario} - {self.chat}"


class Mensaje(models.Model):
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.contenido[:50]


class Notificacion(models.Model):
    TIPO_CHOICES = [
        ("amistad", "Amistad"),
        ("comentario", "Comentario"),
        ("mensaje", "Mensaje"),
        ("grupo", "Grupo"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo} - {self.usuario}"