from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 3: detalle de usuario; parámetro entero
    path("usuarios/<int:usuario_id>/", views.detalle_usuario, name="usuario_detalle"),
]
