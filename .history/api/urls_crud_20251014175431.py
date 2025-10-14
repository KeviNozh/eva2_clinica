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
    path('medicos/editar/<int:id>/', views_crud.editar_medico, name='editar_medico'),
    path('medicos/eliminar/<int:id>/', views_crud.eliminar_medico, name='eliminar_medico'),

    # Especialidades
    path('especialidades/', views_crud.crud_especialidades, name='crud_especialidades'),
    path('especialidades/crear/', views_crud.crear_especialidad, name='crear_especialidad'),
    path('especialidades/editar/<int:id>/', views_crud.editar_especialidad, name='editar_especialidad'),
    path('especialidades/eliminar/<int:id>/', views_crud.eliminar_especialidad, name='eliminar_especialidad'),
    
    # Consultas
    path('consultas/', views_crud.crud_consultas, name='crud_consultas'),
    path('consultas/crear/', views_crud.crear_consulta, name='crear_consulta'),
    path('consultas/editar/<int:id>/', views_crud.editar_consulta, name='editar_consulta'),
    path('consultas/eliminar/<int:id>/', views_crud.eliminar_consulta, name='eliminar_consulta'),
    
    # Medicamentos
    path('medicamentos/', views_crud.crud_medicamentos, name='crud_medicamentos'),
    path('medicamentos/crear/', views_crud.crear_medicamento, name='crear_medicamento'),
    path('medicamentos/editar/<int:id>/', views_crud.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/eliminar/<int:id>/', views_crud.eliminar_medicamento, name='eliminar_medicamento'),
    
    # Tratamientos
    path('tratamientos/', views_crud.crud_tratamientos, name='crud_tratamientos'),
    path('tratamientos/crear/', views_crud.crear_tratamiento, name='crear_tratamiento'),
    path('tratamientos/editar/<int:id>/', views_crud.editar_tratamiento, name='editar_tratamiento'),
    path('tratamientos/eliminar/<int:id>/', views_crud.eliminar_tratamiento, name='eliminar_tratamiento'),
        path('crud/tratamientos/crear/', views_crud.crear_tratamiento, name='crear_tratamiento')
    
    # Recetas
    path('recetas/', views_crud.crud_recetas, name='crud_recetas'),
    path('recetas/crear/', views_crud.crear_receta, name='crear_receta'),
    path('recetas/editar/<int:id>/', views_crud.editar_receta, name='editar_receta'),
    path('recetas/eliminar/<int:id>/', views_crud.eliminar_receta, name='eliminar_receta'),
    
    # Salas
    path('salas/', views_crud.crud_salas, name='crud_salas'),
    path('salas/crear/', views_crud.crear_sala, name='crear_sala'),
    path('salas/editar/<int:id>/', views_crud.editar_sala, name='editar_sala'),
    path('salas/eliminar/<int:id>/', views_crud.eliminar_sala, name='eliminar_sala'),
    
    # Seguimientos (MEJORA 2)
    path('seguimientos/', views_crud.crud_seguimientos, name='crud_seguimientos'),
    path('seguimientos/crear/', views_crud.crear_seguimiento, name='crear_seguimiento'),
    path('seguimientos/editar/<int:id>/', views_crud.editar_seguimiento, name='editar_seguimiento'),
    path('seguimientos/eliminar/<int:id>/', views_crud.eliminar_seguimiento, name='eliminar_seguimiento'),
]