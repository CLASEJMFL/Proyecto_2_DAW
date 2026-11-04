from django.urls import path, re_path
from . import views

urlpatterns = [
    # URL 1: página principal
    path("", views.index, name="index"),
]

# Errores
handler400 = 'core.views.error400'
handler403 = 'core.views.error403'
handler404 = 'core.views.error404'
handler500 = 'core.views.error500'