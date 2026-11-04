from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 7: listado de noticias
    path("noticias/", views.lista_noticias, name="noticias"),
]
