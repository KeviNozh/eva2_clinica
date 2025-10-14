"""
VISTAS COMPLETAS CRUD - Operaciones Create, Read, Update, Delete
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import (Especialidad, SalaAtencion, Medico, Paciente, 
                    ConsultaMedica, Tratamiento, Medicamento, RecetaMedica)

# ========== PACIENTES ==========
def crud_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'crud_pacientes.html', {'pacientes': pacientes})

def crear_paciente(request):
    if request.method == 'POST':
        try:
            Paciente.objects.create(
                rut=request.POST['rut'],
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                fecha_nacimiento=request.POST['fecha_nacimiento'],
                genero=request.POST['genero'],
                tipo_sangre=request.POST['tipo_sangre'],
                telefono=request.POST.get('telefono', ''),
                correo=request.POST.get('correo', ''),
                direccion=request.POST.get('direccion', ''),
                activo=True
            )
            messages.success(request, 'Paciente creado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear paciente: {str(e)}')
    return redirect('crud:crud_pacientes')

def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        try:
            paciente.rut = request.POST['rut']
            paciente.nombre = request.POST['nombre']
            paciente.apellido = request.POST['apellido']
            paciente.fecha_nacimiento = request.POST['fecha_nacimiento']
            paciente.genero = request.POST['genero']
            paciente.tipo_sangre = request.POST['tipo_sangre']
            paciente.telefono = request.POST.get('telefono', '')
            paciente.correo = request.POST.get('correo', '')
            paciente.direccion = request.POST.get('direccion', '')
            paciente.save()
            messages.success(request, 'Paciente actualizado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al actualizar paciente: {str(e)}')
        return redirect('crud:crud_pacientes')
    
    return render(request, 'editar_paciente.html', {'paciente': paciente})

def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        try:
            paciente.delete()
            messages.success(request, 'Paciente eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar paciente: {str(e)}')
        return redirect('crud:crud_pacientes')
    
    return render(request, 'eliminar_paciente.html', {'paciente': paciente})

# ========== MÉDICOS ==========
def crud_medicos(request):
    medicos = Medico.objects.select_related('especialidad').all()
    especialidades = Especialidad.objects.all()
    return render(request, 'crud_medicos.html', {
        'medicos': medicos,
        'especialidades': especialidades
    })

def crear_medico(request):
    if request.method == 'POST':
        try:
            especialidad = Especialidad.objects.get(id=request.POST['especialidad'])
            Medico.objects.create(
                rut=request.POST['rut'],
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                correo=request.POST.get('correo', ''),
                telefono=request.POST.get('telefono', ''),
                especialidad=especialidad,
                activo=True
            )
            messages.success(request, 'Médico creado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear médico: {str(e)}')
    return redirect('crud:crud_medicos')

def editar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    especialidades = Especialidad.objects.all()
    
    if request.method == 'POST':
        try:
            medico.rut = request.POST['rut']
            medico.nombre = request.POST['nombre']
            medico.apellido = request.POST['apellido']
            medico.correo = request.POST.get('correo', '')
            medico.telefono = request.POST.get('telefono', '')
            medico.especialidad = Especialidad.objects.get(id=request.POST['especialidad'])
            medico.save()
            messages.success(request, 'Médico actualizado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al actualizar médico: {str(e)}')
        return redirect('crud:crud_medicos')
    
    return render(request, 'editar_medico.html', {
        'medico': medico,
        'especialidades': especialidades
    })

def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        try:
            medico.delete()
            messages.success(request, 'Médico eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar médico: {str(e)}')
        return redirect('crud:crud_medicos')
    
    return render(request, 'eliminar_medico.html', {'medico': medico})

# ========== CONSULTAS MÉDICAS ==========
def crud_consultas(request):
    consultas = ConsultaMedica.objects.select_related('paciente', 'medico', 'sala').all()
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    salas = SalaAtencion.objects.all()
    return render(request, 'crud_consultas.html', {
        'consultas': consultas,
        'pacientes': pacientes,
        'medicos': medicos,
        'salas': salas
    })

def crear_consulta(request):
    if request.method == 'POST':
        try:
            paciente = Paciente.objects.get(id=request.POST['paciente'])
            medico = Medico.objects.get(id=request.POST['medico'])
            sala = SalaAtencion.objects.get(id=request.POST['sala']) if request.POST.get('sala') else None
            
            ConsultaMedica.objects.create(
                paciente=paciente,
                medico=medico,
                sala=sala,
                fecha_consulta=request.POST['fecha_consulta'],
                motivo=request.POST['motivo'],
                diagnostico=request.POST.get('diagnostico', ''),
                estado=request.POST.get('estado', 'Programada')
            )
            messages.success(request, 'Consulta creada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear consulta: {str(e)}')
    return redirect('crud:crud_consultas')

# ... Agregar funciones similares para editar_consulta y eliminar_consulta

# ========== URLs actualizadas en urls_crud.py ==========
"""
Agregar estas URLs adicionales:
"""

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
    
    # Consultas
    path('consultas/', views_crud.crud_consultas, name='crud_consultas'),
    path('consultas/crear/', views_crud.crear_consulta, name='crear_consulta'),
    # ... agregar editar y eliminar para consultas
    
    # Repetir patrón para las demás entidades
]