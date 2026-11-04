from django.shortcuts import render
from .models import *

# Create your views here.









# Errores:

def error_400(request, exception=None):
    return render(request, 'core/errores/400.html', status=400)

def error_403(request, exception=None):
    return render(request, 'core/errores/403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'core/errores/405.html', status=404)

def error_500(request, exception=None):
    return render(request, 'core/errores/500.html', status=500)