"""
VISTAS PARA LOS TEMPLATES CRUD - Conexión real con PostgreSQL
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import (Especialidad, SalaAtencion, Medico, Paciente, 
                    ConsultaMedica, Tratamiento, Medicamento, RecetaMedica)

# Vistas para Pacientes
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
    return redirect('crud_pacientes')

# Vistas para Médicos
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
    return redirect('crud_medicos')

# Vistas para Especialidades
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
    return redirect('crud_especialidades')

# Vistas para Consultas Médicas
def crud_consultas(request):
    consultas = ConsultaMedica.objects.select_related('paciente', 'medico').all()
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    return render(request, 'crud_consultas.html', {
        'consultas': consultas,
        'pacientes': pacientes,
        'medicos': medicos
    })

# Vistas para Medicamentos
def crud_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'crud_medicamentos.html', {'medicamentos': medicamentos})

def crear_medicamento(request):
    if request.method == 'POST':
        try:
            Medicamento.objects.create(
                nombre=request.POST['nombre'],
                laboratorio=request.POST.get('laboratorio', ''),
                stock=request.POST.get('stock', 0),
                precio_unitario=request.POST.get('precio_unitario', 0),
                tipo=request.POST.get('tipo', 'Tableta')
            )
            messages.success(request, 'Medicamento creado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear medicamento: {str(e)}')
    return redirect('crud_medicamentos')

# Vistas para Tratamientos
def crud_tratamientos(request):
    tratamientos = Tratamiento.objects.select_related('consulta').all()
    return render(request, 'crud_tratamientos.html', {'tratamientos': tratamientos})

# Vistas para Recetas
def crud_recetas(request):
    recetas = RecetaMedica.objects.select_related('consulta', 'medicamento').all()
    return render(request, 'crud_recetas.html', {'recetas': recetas})

# Vistas para Salas
def crud_salas(request):
    salas = SalaAtencion.objects.all()
    return render(request, 'crud_salas.html', {'salas': salas})

def crear_sala(request):
    if request.method == 'POST':
        try:
            SalaAtencion.objects.create(
                numero_sala=request.POST['numero_sala'],
                piso=request.POST['piso'],
                tipo_sala=request.POST['tipo_sala'],
                disponibilidad=request.POST.get('disponibilidad', True)
            )
            messages.success(request, 'Sala creada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear sala: {str(e)}')
    return redirect('crud_salas')