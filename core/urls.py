from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 5: listado de grupos
    path("grupos/", views.lista_grupos, name="grupos"),
]
