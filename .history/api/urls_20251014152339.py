"""
URLS PARA LA API DEL SISTEMA SALUD VITAL
Configuración de endpoints y documentación
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views

# Configuración de documentación
schema_view = get_schema_view(
    openapi.Info(
        title="Sistema Salud Vital - API",
        default_version='v1',
        description="Documentación completa del API para el sistema de gestión médica",
        contact=openapi.Contact(email="admin@clinicavital.cl"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Configuración del router para la API
router = DefaultRouter()
router.register(r'especialidades', views.EspecialidadViewSet)
router.register(r'salas', views.SalaViewSet)
router.register(r'medicos', views.MedicoViewSet)
router.register(r'pacientes', views.PacienteViewSet)
router.register(r'consultas', views.ConsultaViewSet)
router.register(r'medicamentos', views.MedicamentoViewSet)
router.register(r'tratamientos', views.TratamientoViewSet)
router.register(r'recetas', views.RecetaViewSet)
router.register(r'seguimientos', views.SeguimientoPacienteViewSet)

urlpatterns = [
    # Endpoints de la API
    path('', include(router.urls)),
    
    # Documentación
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-docs'),
    
    # URLs CRUD para Salas
    path('salas/crear/', views.crear_sala, name='crear_sala'),
    path('salas/editar/<int:id>/', views.editar_sala, name='editar_sala'),
    path('salas/eliminar/<int:id>/', views.eliminar_sala, name='eliminar_sala'),
    path('salas/', views.lista_salas, name='crud_salas'),
    
    # Otras URLs CRUD
    path('especialidades/crear/', views.crear_especialidad, name='crear_especialidad'),
    path('especialidades/', views.lista_especialidades, name='crud_especialidades'),
    
    # ... (mantener tus otras URLs existentes)
]