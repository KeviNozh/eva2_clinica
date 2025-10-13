"""
URL configuration for salud_vital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
router.register(r'salas-atencion', views.SalaAtencionViewSet)
router.register(r'medicos', views.MedicoViewSet)
router.register(r'pacientes', views.PacienteViewSet)
router.register(r'consultas-medicas', views.ConsultaMedicaViewSet)
router.register(r'tratamientos', views.TratamientoViewSet)
router.register(r'medicamentos', views.MedicamentoViewSet)
router.register(r'recetas-medicas', views.RecetaMedicaViewSet)

urlpatterns = [
    # Endpoints de la API
    path('api/', include(router.urls)),
    
    # Documentación de la API
    path('docs/', include_docs_urls(
        title='Sistema Salud Vital - API',
        description='Documentación completa de la API para el sistema de gestión médica'
    )),
    
    # Autenticación de la API
    path('api-auth/', include('rest_framework.urls')),
]