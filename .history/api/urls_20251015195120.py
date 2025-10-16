"""
URLS PARA LA API DEL SISTEMA SALUD VITAL
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views
from . import views_crud  # Para las vistas CRUD
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
    path('crud/tratamientos/', views_crud.crud_tratamientos, name='crud_tratamientos'),
    path('crud/tratamientos/crear/', views_crud.crear_tratamiento, name='crear_tratamiento'),
    path('crud/consultas/crear/', views_crud.crear_consulta, name='crear_consulta'),
    path('crud/consultas/', views_crud.crud_consultas, name='crud_consultas'),
    path('crud/consultas/crear/', views_crud.crear_consulta, name='crear_consulta'),
    path('crud/consultas/editar/<int:id>/', views_crud.editar_consulta, name='editar_consulta'),
    path('crud/consultas/eliminar/<int:id>/', views_crud.eliminar_consulta, name='eliminar_consulta'),
    path('crud/recetas/', views_crud.crud_recetas, name='crud_recetas'),
    path('crud/recetas/crear/', views_crud.crear_receta, name='crear_receta'),
    path('crud/recetas/editar/<int:id>/', views_crud.editar_receta, name='editar_receta'),
    path('crud/recetas/eliminar/<int:id>/', views_crud.eliminar_receta, name='eliminar_receta'),
# Agrega estas líneas a tu urlpatterns:
    path('crud/tratamientos/editar/<int:id>/', views_crud.editar_tratamiento, name='editar_tratamiento'),
    path('crud/tratamientos/eliminar/<int:id>/', views_crud.eliminar_tratamiento, name='eliminar_tratamiento'),
    path('especialidades/editar/<int:id>/', views.editar_especialidad, name='editar_especialidad'),
]
