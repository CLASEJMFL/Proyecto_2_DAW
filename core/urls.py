from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 8: detalle de noticia; parámetro entero
    path("noticias/<int:noticia_id>/", views.detalle_noticia, name="noticia_detalle"),
]
