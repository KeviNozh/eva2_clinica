"""
VISTAS PARA LOS TEMPLATES CRUD - Funciones completas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Especialidad, Medico

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