from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 6: dos parámetros: entero (grupo_id) y texto (rol)
    path(
        "grupos/<int:grupo_id>/<str:rol>/",
        views.detalle_grupo,
        name="grupo_detalle",
    ),
]
