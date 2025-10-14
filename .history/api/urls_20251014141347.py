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

# Configuración de documentación con drf-yasg
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
    
    # Documentación moderna
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-docs'),
    
    # Documentación JSON/YAML
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
        path('crud/especialidades/crear/', views.crear_especialidad, name='crear_especialidad'),
    path('crud/especialidades/', views.lista_especialidades, name='crud_especialidades'),
    
    path('crud/pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('crud/pacientes/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('crud/pacientes/eliminar/<int:id>/', views.eliminar_paciente, name='eliminar_paciente'),
    path('crud/pacientes/', views.lista_pacientes, name='crud_pacientes'),
    
    path('crud/medicos/crear/', views.crear_medico, name='crear_medico'),
    
    path('crud/medicamentos/crear/', views.crear_medicamento, name='crear_medicamento'),
    path('crud/medicamentos/eliminar/<int:id>/', views.eliminar_medicamento, name='eliminar_medicamento'),
    path('crud/medicamentos/', views.lista_medicamentos, name='crud_medicamentos'),
]