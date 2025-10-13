"""
URLS PARA LA API DEL SISTEMA SALUD VITAL
Configuración de endpoints y documentación
"""
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views

# Configuración del router para la API
router = routers.DefaultRouter()
router.register(r'especialidades', views.EspecialidadViewSet)
router.register(r'medicos', views.MedicoViewSet)
router.register(r'pacientes', views.PacienteViewSet)
# ... registrar todos los modelos

urlpatterns = [
    # Endpoints de la API
    path('', include(router.urls)),
    
    # Documentación de la API
    path('docs/', include_docs_urls(title='Sistema Salud Vital - API')),
]