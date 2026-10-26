import random
from faker import Faker

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    Usuario,
    Amistad,
    Grupo,
    Pertenencia,
    Juego,
    Noticia,
    Comentario,
    Reaccion,
    UsuarioJuego,
    Chat,
    ParticipanteChat,
    Mensaje,
    Notificacion,
)


fake = Faker("es_ES")


class Command(BaseCommand):
    help = "Genera 10 registros de prueba por modelo"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        usuarios = []
        grupos = []
        juegos = []
        noticias = []
        chats = []

        # 1. Crear 10 usuarios
        for i in range(10):
            usuario = Usuario.objects.create_user(
                username=f"usuario{i + 1}",
                email=f"usuario{i + 1}@example.com",
                password="Prueba123!",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                biografia=fake.text(max_nb_chars=100),
                foto_perfil=fake.image_url(),
            )
            usuarios.append(usuario)

        # 2. Crear 10 grupos
        for i in range(10):
            grupo = Grupo.objects.create(
                nombre=f"Grupo {i + 1}",
                descripcion=fake.text(max_nb_chars=150),
                imagen=fake.image_url(),
            )
            grupos.append(grupo)

        # 3. Crear 10 juegos
        for i in range(10):
            juego = Juego.objects.create(
                nombre=fake.unique.catch_phrase(),
                descripcion=fake.text(max_nb_chars=150),
                genero=random.choice([
                    "Acción", "Aventura", "RPG", "Deportes",
                    "Estrategia", "Terror"
                ]),
                imagen=fake.image_url(),
                plataformas=random.choice([
                    "PC", "PS5", "Xbox", "Nintendo Switch"
                ]),
            )
            juegos.append(juego)

        # 4. Crear 10 pertenencias
        for i in range(10):
            Pertenencia.objects.create(
                usuario=usuarios[i],
                grupo=grupos[i],
                rol="miembro",
            )

        # 5. Crear 10 amistades
        for i in range(10):
            Amistad.objects.create(
                usuario_origen=usuarios[i],
                usuario_destino=usuarios[(i + 1) % 10],
            )

        # 6. Crear 10 noticias
        for i in range(10):
            noticia = Noticia.objects.create(
                titulo=fake.sentence(),
                contenido=fake.text(max_nb_chars=300),
                autor=usuarios[i],
                grupo=grupos[i],
                juego=juegos[i],
            )
            noticias.append(noticia)

        # 7. Crear 10 comentarios
        for i in range(10):
            Comentario.objects.create(
                contenido=fake.sentence(),
                usuario=usuarios[i],
                noticia=noticias[i],
            )

        # 8. Crear 10 reacciones
        for i in range(10):
            Reaccion.objects.create(
                tipo=random.choice(["me_gusta", "no_me_gusta"]),
                usuario=usuarios[i],
                noticia=noticias[i],
            )

        # 9. Crear 10 relaciones entre usuarios y juegos
        for i in range(10):
            UsuarioJuego.objects.create(
                usuario=usuarios[i],
                juego=juegos[i],
                horas_jugadas=random.randint(0, 500),
                favorito=random.choice([True, False]),
            )

        # 10. Crear 10 chats
        for i in range(10):
            chat = Chat.objects.create(
                tipo="privado",
                nombre=f"Chat {i + 1}",
            )
            chats.append(chat)

        # 11. Crear 10 participantes de chat
        for i in range(10):
            ParticipanteChat.objects.create(
                usuario=usuarios[i],
                chat=chats[i],
                rol="miembro",
            )

        # 12. Crear 10 mensajes
        for i in range(10):
            Mensaje.objects.create(
                contenido=fake.sentence(),
                autor=usuarios[i],
                chat=chats[i],
            )

        # 13. Crear 10 notificaciones
        for i in range(10):
            Notificacion.objects.create(
                tipo="comentario",
                mensaje=fake.sentence(),
                usuario=usuarios[i],
                leida=False,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "¡Seeder ejecutado! Se han creado los datos de prueba."
            )
        )