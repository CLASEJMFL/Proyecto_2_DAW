from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 9: estadísticas y filtro de agregación
    path("estadisticas/", views.estadisticas, name="estadisticas"),

]
