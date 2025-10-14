"""
VISTAS PARA LOS TEMPLATES CRUD - Funciones completas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Especialidad, Medico, Paciente  # agrega Paciente si no está importado

# MEDICOS
def crear_medico(request):
    if request.method == 'POST':
        try:
            esp_id = request.POST.get('especialidad') or None
            esp = get_object_or_404(Especialidad, id=esp_id) if esp_id else None
            Medico.objects.create(
                rut=request.POST.get('rut', '').strip(),
                nombre=request.POST.get('nombre', '').strip(),
                apellido=request.POST.get('apellido', '').strip(),
                telefono=request.POST.get('telefono', '').strip(),
                correo=request.POST.get('correo', '').strip(),
                especialidad=esp
            )
            messages.success(request, 'Médico creado.')
            return redirect('crud:crud_medicos')
        except Exception as e:
            messages.error(request, f'Error creando médico: {e}')
    especialidades = Especialidad.objects.all()
    return render(request, 'crear_medico.html', {'especialidades': especialidades})

def editar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        try:
            medico.rut = request.POST.get('rut', medico.rut).strip()
            medico.nombre = request.POST.get('nombre', medico.nombre).strip()
            medico.apellido = request.POST.get('apellido', medico.apellido).strip()
            medico.telefono = request.POST.get('telefono', medico.telefono).strip()
            medico.correo = request.POST.get('correo', medico.correo).strip()
            esp_id = request.POST.get('especialidad') or None
            medico.especialidad = get_object_or_404(Especialidad, id=esp_id) if esp_id else None
            medico.save()
            messages.success(request, 'Médico actualizado.')
            return redirect('crud:crud_medicos')
        except Exception as e:
            messages.error(request, f'Error actualizando médico: {e}')
    especialidades = Especialidad.objects.all()
    return render(request, 'editar_medico.html', {'medico': medico, 'especialidades': especialidades})

def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        try:
            medico.delete()
            messages.success(request, 'Médico eliminado.')
            return redirect('crud:crud_medicos')
        except Exception as e:
            messages.error(request, f'Error eliminando médico: {e}')
    return render(request, 'eliminar_medico.html', {'medico': medico})

# ESPECIALIDADES
def crud_especialidades(request):
    especialidades = Especialidad.objects.all()
    q = request.GET.get('q', '')
    if q:
        especialidades = especialidades.filter(nombre__icontains=q)
    return render(request, 'crud_especialidades.html', {'especialidades': especialidades})

def crear_especialidad(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            if not nombre:
                messages.error(request, 'Nombre requerido.')
            else:
                Especialidad.objects.create(nombre=nombre, descripcion=descripcion)
                messages.success(request, 'Especialidad creada.')
                return redirect('crud:crud_especialidades')
        except Exception as e:
            messages.error(request, f'Error creando especialidad: {e}')
    return render(request, 'crear_especialidad.html')

def editar_especialidad(request, id):
    esp = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        try:
            esp.nombre = request.POST.get('nombre', esp.nombre).strip()
            esp.descripcion = request.POST.get('descripcion', esp.descripcion).strip()
            esp.save()
            messages.success(request, 'Especialidad actualizada.')
            return redirect('crud:crud_especialidades')
        except Exception as e:
            messages.error(request, f'Error actualizando especialidad: {e}')
    return render(request, 'editar_especialidad.html', {'especialidad': esp})

def eliminar_especialidad(request, id):
    esp = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        try:
            esp.delete()
            messages.success(request, 'Especialidad eliminada.')
            return redirect('crud:crud_especialidades')
        except Exception as e:
            messages.error(request, f'Error eliminando especialidad: {e}')
    return render(request, 'eliminar_especialidad.html', {'especialidad': esp})

# PACIENTES
def crud_pacientes(request):
    pacientes = Paciente.objects.all()
    q = request.GET.get('q', '')
    if q:
        pacientes = pacientes.filter(
            Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(rut__icontains=q)
        )
    return render(request, 'crud_pacientes.html', {'pacientes': pacientes})

def crear_paciente(request):
    if request.method == 'POST':
        try:
            Paciente.objects.create(
                rut=request.POST.get('rut', '').strip(),
                nombre=request.POST.get('nombre', '').strip(),
                apellido=request.POST.get('apellido', '').strip(),
                fecha_nacimiento=request.POST.get('fecha_nacimiento') or None,
                telefono=request.POST.get('telefono', '').strip(),
                correo=request.POST.get('correo', '').strip(),
                direccion=request.POST.get('direccion', '').strip()
            )
            messages.success(request, 'Paciente creado.')
            return redirect('crud:crud_pacientes')
        except Exception as e:
            messages.error(request, f'Error creando paciente: {e}')
    return render(request, 'crear_paciente.html')

def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        try:
            paciente.rut = request.POST.get('rut', paciente.rut).strip()
            paciente.nombre = request.POST.get('nombre', paciente.nombre).strip()
            paciente.apellido = request.POST.get('apellido', paciente.apellido).strip()
            paciente.fecha_nacimiento = request.POST.get('fecha_nacimiento') or paciente.fecha_nacimiento
            paciente.telefono = request.POST.get('telefono', paciente.telefono).strip()
            paciente.correo = request.POST.get('correo', paciente.correo).strip()
            paciente.direccion = request.POST.get('direccion', paciente.direccion).strip()
            paciente.save()
            messages.success(request, 'Paciente actualizado.')
            return redirect('crud:crud_pacientes')
        except Exception as e:
            messages.error(request, f'Error actualizando paciente: {e}')
    return render(request, 'editar_paciente.html', {'paciente': paciente})

def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        try:
            paciente.delete()
            messages.success(request, 'Paciente eliminado.')
            return redirect('crud:crud_pacientes')
        except Exception as e:
            messages.error(request, f'Error eliminando paciente: {e}')
    return render(request, 'eliminar_paciente.html', {'paciente': paciente})