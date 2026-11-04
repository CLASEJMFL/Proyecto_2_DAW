from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 2: listado de usuarios
    path("usuarios/", views.lista_usuarios, name="usuarios"),
]
