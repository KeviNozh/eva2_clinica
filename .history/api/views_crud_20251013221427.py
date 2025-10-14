"""
VISTAS PARA LOS TEMPLATES CRUD - Funciones completas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import (Especialidad, SalaAtencion, Medico, Paciente, 
                    ConsultaMedica, Tratamiento, Medicamento, RecetaMedica)
# En api/views_crud.py, agrega esto:
from django.http import HttpResponse

def crud_consultas(request):
    return HttpResponse("¡Hola mundo desde crud_consultas!")
# ========== PACIENTES ==========
def crud_pacientes(request):
    pacientes = Paciente.objects.all()
    
    # Filtros
    q = request.GET.get('q', '')
    genero = request.GET.get('genero', '')
    tipo_sangre = request.GET.get('tipo_sangre', '')
    activo = request.GET.get('activo', '')
    
    if q:
        pacientes = pacientes.filter(
            Q(nombre__icontains=q) | 
            Q(apellido__icontains=q) | 
            Q(rut__icontains=q)
        )
    if genero:
        pacientes = pacientes.filter(genero=genero)
    if tipo_sangre:
        pacientes = pacientes.filter(tipo_sangre=tipo_sangre)
    if activo:
        pacientes = pacientes.filter(activo=(activo == 'true'))
    
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
    
    return render(request, 'crear_paciente.html')

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
            return redirect('crud:crud_pacientes')
        except Exception as e:
            messages.error(request, f'Error al actualizar paciente: {str(e)}')
    
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
    
    # Filtros
    q = request.GET.get('q', '')
    especialidad = request.GET.get('especialidad', '')
    
    if q:
        medicos = medicos.filter(
            Q(nombre__icontains=q) | 
            Q(apellido__icontains=q) | 
            Q(rut__icontains=q)
        )
    if especialidad:
        medicos = medicos.filter(especialidad__nombre__icontains=especialidad)
    
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
    
    especialidades = Especialidad.objects.all()
    return render(request, 'crear_medico.html', {'especialidades': especialidades})

# ========== ESPECIALIDADES ==========
def crud_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'crud_especialidades.html', {'especialidades': especialidades})

def crear_especialidad(request):
    if request.method == 'POST':
        try:
            Especialidad.objects.create(
                nombre=request.POST['nombre'],
                descripcion=request.POST.get('descripcion', '')
            )
            messages.success(request, 'Especialidad creada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear especialidad: {str(e)}')
        return redirect('crud:crud_especialidades')
    
    return render(request, 'crear_especialidad.html')

def crud_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'crud_medicamentos.html', {'medicamentos': medicamentos})