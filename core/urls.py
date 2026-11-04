from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 4: listado de juegos
    path("juegos/", views.lista_juegos, name="juegos"),
]
