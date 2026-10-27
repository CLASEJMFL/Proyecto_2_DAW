from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import (
    Usuario, Amistad, Grupo, Pertenencia, Juego,
    Noticia, Comentario, Reaccion, UsuarioJuego,
    Chat, ParticipanteChat, Mensaje, Notificacion
)

admin.site.register(Usuario, UserAdmin)
admin.site.register(Amistad)
admin.site.register(Grupo)
admin.site.register(Pertenencia)
admin.site.register(Juego)
admin.site.register(Noticia)
admin.site.register(Comentario)
admin.site.register(Reaccion)
admin.site.register(UsuarioJuego)
admin.site.register(Chat)
admin.site.register(ParticipanteChat)
admin.site.register(Mensaje)
admin.site.register(Notificacion)