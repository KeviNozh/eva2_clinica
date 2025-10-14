"""
URLS PARA LA API DEL SISTEMA SALUD VITAL
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views
from . import views_crud

app_name = 'crud'

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
    
    # URLs CRUD para templates
    # ========== LISTAR ==========
    path('pacientes/', views_crud.crud_pacientes, name='crud_pacientes'),
    path('medicos/', views_crud.crud_medicos, name='crud_medicos'),
    path('medicamentos/', views_crud.crud_medicamentos, name='crud_medicamentos'),
    path('especialidades/', views_crud.crud_especialidades, name='crud_especialidades'),
    path('consultas/', views_crud.crud_consultas, name='crud_consultas'),
    path('recetas/', views_crud.crud_recetas, name='crud_recetas'),
    path('tratamientos/', views_crud.crud_tratamientos, name='crud_tratamientos'),
    path('salas/', views_crud.crud_salas, name='crud_salas'),
    path('seguimientos/', views_crud.crud_seguimientos, name='crud_seguimientos'),
    
    # ========== CREAR ==========
    path('pacientes/crear/', views_crud.crear_paciente, name='crear_paciente'),
    path('medicos/crear/', views_crud.crear_medico, name='crear_medico'),
    path('medicamentos/crear/', views_crud.crear_medicamento, name='crear_medicamento'),
    path('especialidades/crear/', views_crud.crear_especialidad, name='crear_especialidad'),
    path('salas/crear/', views_crud.crear_sala, name='crear_sala'),
    path('consultas/crear/', views_crud.crear_consulta, name='crear_consulta'),
    path('tratamientos/crear/', views_crud.crear_tratamiento, name='crear_tratamiento'),
    path('recetas/crear/', views_crud.crear_receta, name='crear_receta'),
    path('seguimientos/crear/', views_crud.crear_seguimiento, name='crear_seguimiento'),
    
    # ========== EDITAR ==========
    path('pacientes/editar/<int:id>/', views_crud.editar_paciente, name='editar_paciente'),
    path('medicos/editar/<int:id>/', views_crud.editar_medico, name='editar_medico'),
    path('medicamentos/editar/<int:id>/', views_crud.editar_medicamento, name='editar_medicamento'),
    path('especialidades/editar/<int:id>/', views_crud.editar_especialidad, name='editar_especialidad'),
    path('salas/editar/<int:id>/', views_crud.editar_sala, name='editar_sala'),
    path('consultas/editar/<int:id>/', views_crud.editar_consulta, name='editar_consulta'),
    path('tratamientos/editar/<int:id>/', views_crud.editar_tratamiento, name='editar_tratamiento'),
    path('recetas/editar/<int:id>/', views_crud.editar_receta, name='editar_receta'),
    path('seguimientos/editar/<int:id>/', views_crud.editar_seguimiento, name='editar_seguimiento'),
    
    # ========== ELIMINAR ==========
    path('pacientes/eliminar/<int:id>/', views_crud.eliminar_paciente, name='eliminar_paciente'),
    path('medicos/eliminar/<int:id>/', views_crud.eliminar_medico, name='eliminar_medico'),
    path('medicamentos/eliminar/<int:id>/', views_crud.eliminar_medicamento, name='eliminar_medicamento'),
    path('especialidades/eliminar/<int:id>/', views_crud.eliminar_especialidad, name='eliminar_especialidad'),
    path('salas/eliminar/<int:id>/', views_crud.eliminar_sala, name='eliminar_sala'),
    path('consultas/eliminar/<int:id>/', views_crud.eliminar_consulta, name='eliminar_consulta'),
    path('tratamientos/eliminar/<int:id>/', views_crud.eliminar_tratamiento, name='eliminar_tratamiento'),
    path('recetas/eliminar/<int:id>/', views_crud.eliminar_receta, name='eliminar_receta'),
    path('seguimientos/eliminar/<int:id>/', views_crud.eliminar_seguimiento, name='eliminar_seguimiento'),
    
    # Documentación
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-docs'),
]