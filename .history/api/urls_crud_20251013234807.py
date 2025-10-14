"""
URLS PARA LAS VISTAS CRUD - Completo
"""
from django.urls import path
from . import views_crud

app_name = 'crud'

urlpatterns = [
    # Pacientes
    path('pacientes/', views_crud.crud_pacientes, name='crud_pacientes'),
    path('pacientes/crear/', views_crud.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:id>/', views_crud.editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:id>/', views_crud.eliminar_paciente, name='eliminar_paciente'),
    
    # Médicos
    path('medicos/', views_crud.crud_medicos, name='crud_medicos'),
    path('medicos/crear/', views_crud.crear_medico, name='crear_medico'),
    
    # Especialidades
    path('especialidades/', views_crud.crud_especialidades, name='crud_especialidades'),
    path('especialidades/crear/', views_crud.crear_especialidad, name='crear_especialidad'),
    
    # Consultas
    path('consultas/', views_crud.crud_consultas, name='crud_consultas'),
    
    # Medicamentos
    path('medicamentos/', views_crud.crud_medicamentos, name='crud_medicamentos'),
    path('medicamentos/crear/', views_crud.crear_medicamento, name='crear_medicamento'),
    
    # Tratamientos
    path('tratamientos/', views_crud.crud_tratamientos, name='crud_tratamientos'),
    
    # Recetas
    path('recetas/', views_crud.crud_recetas, name='crud_recetas'),
    
    # Salas
    path('salas/', views_crud.crud_salas, name='crud_salas'),
    path('salas/crear/', views_crud.crear_sala, name='crear_sala'),
]