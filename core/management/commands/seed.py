import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from core.models import (
    Usuario,
    PerfilUsuario,
    ConfiguracionUsuario,
    EstadisticasUsuario,
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
    help = "Genera 10 registros de prueba por modelo de GameLoop por ejecución."

    @transaction.atomic
    def handle(self, *args, **options):
        # Se crean 10 usuarios nuevos; los nombres se hacen únicos.
        usuarios = []
        for i in range(10):
            username = self._unique_username(i)
            usuario = Usuario.objects.create_user(
                username=username,
                email=fake.unique.email(),
                password="GameLoopDemo123!",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                foto_perfil=fake.image_url(),
                biografia=fake.text(max_nb_chars=180),
            )
            usuarios.append(usuario)

        perfiles = [
            PerfilUsuario.objects.create(
                usuario=usuario,
                nombre_visible=fake.name(),
                biografia=fake.text(max_nb_chars=160),
                fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=65),
                web=fake.url(),
            )
            for usuario in usuarios
        ]

        configuraciones = [
            ConfiguracionUsuario.objects.create(
                usuario=usuario,
                tema_oscuro=random.choice([True, False]),
                notificaciones_activadas=random.choice([True, False]),
                idioma=random.choice(["es", "en"]),
            )
            for usuario in usuarios
        ]

        estadisticas = [
            EstadisticasUsuario.objects.create(
                usuario=usuario,
                juegos_favoritos=random.randint(0, 30),
                horas_totales=round(random.uniform(0, 1500), 2),
                nivel=random.randint(1, 100),
                puntuacion_media=round(random.uniform(0, 10), 2),
            )
            for usuario in usuarios
        ]

        juegos = [
            Juego.objects.create(
                nombre=f"{fake.unique.catch_phrase()} {i + 1}",
                descripcion=fake.text(max_nb_chars=250),
                genero=random.choice(
                    ["Acción", "Aventura", "RPG", "Estrategia", "Deportes", "Puzles"]
                ),
                imagen=fake.image_url(),
                fecha_lanzamiento=fake.date_between(
                    start_date="-15y", end_date="today"
                ),
                plataformas=random.choice(
                    ["PC", "PlayStation", "Xbox", "Nintendo Switch", "PC y consola"]
                ),
            )
            for i in range(10)
        ]

        grupos = [
            Grupo.objects.create(
                nombre=f"{fake.unique.word().capitalize()} {i + 1}",
                descripcion=fake.text(max_nb_chars=180),
                imagen=fake.image_url(),
                fecha_creacion=fake.date_time_between(
                    start_date="-2y", end_date="now", tzinfo=timezone.get_current_timezone()
                ),
            )
            for i in range(10)
        ]

        pertenencias = []
        for i in range(10):
            pertenencias.append(
                Pertenencia.objects.create(
                    usuario=usuarios[i],
                    grupo=grupos[i],
                    rol=random.choice(["administrador", "moderador", "miembro"]),
                    fecha_union=timezone.now() - timedelta(days=random.randint(0, 365)),
                )
            )

        # Relaciones muchos-a-muchos de grupos con juegos.
        for grupo in grupos:
            grupo.juegos.add(random.choice(juegos))

        amistades = []
        for i in range(10):
            origen = usuarios[i]
            destino = usuarios[(i + 1) % len(usuarios)]
            amistad, _ = Amistad.objects.get_or_create(
                usuario_origen=origen,
                usuario_destino=destino,
                defaults={
                    "estado": "aceptada",
                    "fecha_solicitud": timezone.now()
                    - timedelta(days=random.randint(1, 180)),
                    "fecha_aceptacion": timezone.now()
                    - timedelta(days=random.randint(0, 90)),
                },
            )
            amistades.append(amistad)

        noticias = []
        for i in range(10):
            noticias.append(
                Noticia.objects.create(
                    titulo=fake.sentence(nb_words=6),
                    contenido=fake.text(max_nb_chars=500),
                    fecha_publicacion=timezone.now()
                    - timedelta(days=random.randint(0, 365)),
                    autor=usuarios[i],
                    grupo=grupos[i],
                    juego=juegos[i],
                )
            )

        comentarios = [
            Comentario.objects.create(
                contenido=fake.sentence(nb_words=12),
                fecha=timezone.now() - timedelta(days=random.randint(0, 90)),
                usuario=usuarios[i],
                noticia=noticias[(i + 1) % len(noticias)],
            )
            for i in range(10)
        ]

        reacciones = []
        for i in range(10):
            reacciones.append(
                Reaccion.objects.create(
                    tipo=random.choice(["me_gusta", "no_me_gusta"]),
                    fecha=timezone.now() - timedelta(days=random.randint(0, 90)),
                    usuario=usuarios[i],
                    noticia=noticias[i],
                )
            )

        usuario_juegos = [
            UsuarioJuego.objects.create(
                usuario=usuarios[i],
                juego=juegos[i],
                horas_jugadas=round(random.uniform(0, 300), 2),
                favorito=random.choice([True, False]),
                fecha_inicio=fake.date_between(start_date="-5y", end_date="today"),
            )
            for i in range(10)
        ]

        chats = []
        for i in range(10):
            chats.append(
                Chat.objects.create(
                    tipo=random.choice(["privado", "grupal"]),
                    fecha_creacion=timezone.now()
                    - timedelta(days=random.randint(0, 180)),
                    nombre=f"Chat {fake.word().capitalize()} {i + 1}",
                )
            )

        participantes = []
        for i, chat in enumerate(chats):
            participantes.append(
                ParticipanteChat.objects.create(
                    usuario=usuarios[i],
                    chat=chat,
                    fecha_union=timezone.now()
                    - timedelta(days=random.randint(0, 90)),
                    rol=random.choice(["administrador", "miembro"]),
                )
            )

        mensajes = [
            Mensaje.objects.create(
                contenido=fake.sentence(nb_words=10),
                fecha_envio=timezone.now()
                - timedelta(minutes=random.randint(1, 100000)),
                autor=usuarios[i],
                chat=chats[i],
            )
            for i in range(10)
        ]

        notificaciones = [
            Notificacion.objects.create(
                tipo=random.choice(["amistad", "comentario", "mensaje", "grupo"]),
                mensaje=fake.sentence(nb_words=10),
                fecha=timezone.now() - timedelta(days=random.randint(0, 60)),
                usuario=usuarios[i],
                leida=random.choice([True, False]),
            )
            for i in range(10)
        ]

        self.stdout.write(
            self.style.SUCCESS(
                "Seed completado: se han generado 10 registros por modelo en esta ejecución."
            )
        )
        self.stdout.write(
            "Contraseña de los usuarios de prueba: GameLoopDemo123!"
        )

    def _unique_username(self, index):
        base = fake.unique.user_name()[:120]
        username = f"{base}_{index}"
        # Evita colisiones con usuarios de ejecuciones anteriores.
        suffix = 1
        candidate = username
        while Usuario.objects.filter(username=candidate).exists():
            candidate = f"{username}_{suffix}"
            suffix += 1
        return candidate
