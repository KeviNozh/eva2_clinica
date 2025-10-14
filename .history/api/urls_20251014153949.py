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
    
    # URLs CRUD COMPLETAS
    
    # Especialidades
    path('especialidades/crear/', views.crear_especialidad, name='crear_especialidad'),
    path('especialidades/editar/<int:id>/', views.editar_especialidad, name='editar_especialidad'),
    path('especialidades/eliminar/<int:id>/', views.eliminar_especialidad, name='eliminar_especialidad'),
    path('especialidades/', views.lista_especialidades, name='crud_especialidades'),
    
    # Salas
    path('salas/crear/', views.crear_sala, name='crear_sala'),
    path('salas/editar/<int:id>/', views.editar_sala, name='editar_sala'),
    path('salas/eliminar/<int:id>/', views.eliminar_sala, name='eliminar_sala'),
    path('salas/', views.lista_salas, name='crud_salas'),
    
    # Médicos
    path('medicos/crear/', views.crear_medico, name='crear_medico'),
    path('medicos/editar/<int:id>/', views.editar_medico, name='editar_medico'),
    path('medicos/eliminar/<int:id>/', views.eliminar_medico, name='eliminar_medico'),
    path('medicos/', views.lista_medicos, name='crud_medicos'),
    
    # Pacientes
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:id>/', views.eliminar_paciente, name='eliminar_paciente'),
    path('pacientes/', views.lista_pacientes, name='crud_pacientes'),
    
    # Medicamentos
    path('medicamentos/crear/', views.crear_medicamento, name='crear_medicamento'),
    path('medicamentos/editar/<int:id>/', views.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/eliminar/<int:id>/', views.eliminar_medicamento, name='eliminar_medicamento'),
    path('medicamentos/', views.lista_medicamentos, name='crud_medicamentos'),
    
    # Consultas
    path('consultas/crear/', views.crear_consulta, name='crear_consulta'),
    path('consultas/editar/<int:id>/', views.editar_consulta, name='editar_consulta'),
    path('consultas/eliminar/<int:id>/', views.eliminar_consulta, name='eliminar_consulta'),
    path('consultas/', views.lista_consultas, name='crud_consultas'),
    
    # Tratamientos
    path('tratamientos/crear/', views.crear_tratamiento, name='crear_tratamiento'),
    path('tratamientos/editar/<int:id>/', views.editar_tratamiento, name='editar_tratamiento'),
    path('tratamientos/eliminar/<int:id>/', views.eliminar_tratamiento, name='eliminar_tratamiento'),
    path('tratamientos/', views.lista_tratamientos, name='crud_tratamientos'),
    
    # Recetas
    path('recetas/crear/', views.crear_receta, name='crear_receta'),
    path('recetas/editar/<int:id>/', views.editar_receta, name='editar_receta'),
    path('recetas/eliminar/<int:id>/', views.eliminar_receta, name='eliminar_receta'),
    path('recetas/', views.lista_recetas, name='crud_recetas'),
    
    # Seguimientos
    path('seguimientos/crear/', views.crear_seguimiento, name='crear_seguimiento'),
    path('seguimientos/editar/<int:id>/', views.editar_seguimiento, name='editar_seguimiento'),
    path('seguimientos/eliminar/<int:id>/', views.eliminar_seguimiento, name='eliminar_seguimiento'),
    path('seguimientos/', views.lista_seguimientos, name='crud_seguimientos'),
]