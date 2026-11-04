from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 10: expresión regular (re_path) con parámetro de texto
    re_path(
        r"^buscar/juego/(?P<termino>[\w-]+)/$",
        views.buscar_juego,
        name="buscar_juego",
    ),
]
