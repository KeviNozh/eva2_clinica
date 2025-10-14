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
            paciente.rut = request.POST.get('rut', paciente.rut)
            paciente.nombre = request.POST.get('nombre', paciente.nombre)
            paciente.apellido = request.POST.get('apellido', paciente.apellido)
            paciente.fecha_nacimiento = request.POST.get('fecha_nacimiento', paciente.fecha_nacimiento)
            paciente.genero = request.POST.get('genero', paciente.genero)
            paciente.tipo_sangre = request.POST.get('tipo_sangre', paciente.tipo_sangre)
            paciente.telefono = request.POST.get('telefono', paciente.telefono)
            paciente.correo = request.POST.get('correo', paciente.correo)
            paciente.direccion = request.POST.get('direccion', paciente.direccion)
            activo = request.POST.get('activo')
            if activo is not None:
                paciente.activo = (activo.lower() in ['1', 'true', 'on', 'si', 'yes'])
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
            especialidad_id = request.POST.get('especialidad')
            especialidad = None
            if especialidad_id:
                especialidad = get_object_or_404(Especialidad, id=especialidad_id)
            Medico.objects.create(
                rut=request.POST.get('rut', ''),
                nombre=request.POST.get('nombre', ''),
                apellido=request.POST.get('apellido', ''),
                telefono=request.POST.get('telefono', ''),
                correo=request.POST.get('correo', ''),
                especialidad=especialidad
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
            nombre = request.POST.get('nombre', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            if not nombre:
                raise ValueError('El nombre de la especialidad es obligatorio.')
            Especialidad.objects.create(nombre=nombre, descripcion=descripcion)
            messages.success(request, 'Especialidad creada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear especialidad: {str(e)}')
        return redirect('crud:crud_especialidades')
    
    return render(request, 'crear_especialidad.html')

# ========== MEDICAMENTOS ==========
def crud_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'crud_medicamentos.html', {'medicamentos': medicamentos})

def crear_medicamento(request):
    if request.method == 'POST':
        try:
            precio_raw = request.POST.get('precio', '')
            precio = float(precio_raw) if precio_raw != '' else 0.0
            Medicamento.objects.create(
                nombre=request.POST.get('nombre', ''),
                laboratorio=request.POST.get('laboratorio', ''),
                descripcion=request.POST.get('descripcion', ''),
                precio=precio
            )
            messages.success(request, 'Medicamento creado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear medicamento: {str(e)}')
        return redirect('crud:crud_medicamentos')
    return render(request, 'crear_medicamento.html')

def editar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        try:
            medicamento.nombre = request.POST.get('nombre', medicamento.nombre)
            medicamento.descripcion = request.POST.get('descripcion', medicamento.descripcion)
            medicamento.laboratorio = request.POST.get('laboratorio', medicamento.laboratorio)
            precio_raw = request.POST.get('precio', '')
            if precio_raw != '':
                medicamento.precio = float(precio_raw)
            medicamento.save()
            messages.success(request, 'Medicamento actualizado exitosamente!')
            return redirect('crud:crud_medicamentos')
        except Exception as e:
            messages.error(request, f'Error al actualizar medicamento: {str(e)}')
    return render(request, 'editar_medicamento.html', {'medicamento': medicamento})

def eliminar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        try:
            medicamento.delete()
            messages.success(request, 'Medicamento eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar medicamento: {str(e)}')
        return redirect('crud:crud_medicamentos')
    return render(request, 'eliminar_medicamento.html', {'medicamento': medicamento})

# ========== SALAS ==========
def crud_salas(request):
    salas = SalaAtencion.objects.all()
    return render(request, 'crud_salas.html', {'salas': salas})

def crear_sala(request):
    if request.method == 'POST':
        try:
            capacidad_raw = request.POST.get('capacidad', '0')
            try:
                capacidad = int(capacidad_raw)
            except ValueError:
                capacidad = 0
            SalaAtencion.objects.create(
                nombre=request.POST.get('nombre', ''),
                descripcion=request.POST.get('descripcion', ''),
                capacidad=capacidad
            )
            messages.success(request, 'Sala creada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear sala: {str(e)}')
        return redirect('crud:crud_salas')
    return render(request, 'crear_sala.html')