"""
VISTAS PARA LOS TEMPLATES CRUD - Funciones completas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import (Especialidad, SalaAtencion, Medico, Paciente,
                     ConsultaMedica, Tratamiento, Medicamento, RecetaMedica)

def crud_consultas(request):
    return HttpResponse("¡Hola mundo desde crud_consultas!")

# ========== PACIENTES ==========
def crud_pacientes(request):
    pacientes = Paciente.objects.all()
    q = request.GET.get('q', '')
    genero = request.GET.get('genero', '')
    tipo_sangre = request.GET.get('tipo_sangre', '')
    activo = request.GET.get('activo', '')
    if q:
        pacientes = pacientes.filter(Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(rut__icontains=q))
    if genero:
        pacientes = pacientes.filter(genero=genero)
    if tipo_sangre:
        pacientes = pacientes.filter(tipo_sangre=tipo_sangre)
    if activo:
        pacientes = pacientes.filter(activo=(activo.lower() in ['true', '1', 'on', 'si']))
    return render(request, 'crud_pacientes.html', {'pacientes': pacientes})

def crear_paciente(request):
    if request.method == 'POST':
        try:
            activo_val = request.POST.get('activo') in ['on', 'true', '1', 'si']
            Paciente.objects.create(
                rut=request.POST.get('rut', '').strip(),
                nombre=request.POST.get('nombre', '').strip(),
                apellido=request.POST.get('apellido', '').strip(),
                fecha_nacimiento=request.POST.get('fecha_nacimiento') or None,
                genero=request.POST.get('genero', ''),
                tipo_sangre=request.POST.get('tipo_sangre', ''),
                telefono=request.POST.get('telefono', ''),
                correo=request.POST.get('correo', ''),
                direccion=request.POST.get('direccion', ''),
                activo=activo_val
            )
            messages.success(request, 'Paciente creado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear paciente: {e}')
        return redirect('crud:crud_pacientes')
    return render(request, 'crear_paciente.html')

def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        try:
            paciente.rut = request.POST.get('rut', paciente.rut)
            paciente.nombre = request.POST.get('nombre', paciente.nombre)
            paciente.apellido = request.POST.get('apellido', paciente.apellido)
            paciente.fecha_nacimiento = request.POST.get('fecha_nacimiento') or paciente.fecha_nacimiento
            paciente.genero = request.POST.get('genero', paciente.genero)
            paciente.tipo_sangre = request.POST.get('tipo_sangre', paciente.tipo_sangre)
            paciente.telefono = request.POST.get('telefono', paciente.telefono)
            paciente.correo = request.POST.get('correo', paciente.correo)
            paciente.direccion = request.POST.get('direccion', paciente.direccion)
            activo = request.POST.get('activo')
            if activo is not None:
                paciente.activo = activo in ['on', 'true', '1', 'si']
            paciente.save()
            messages.success(request, 'Paciente actualizado exitosamente!')
            return redirect('crud:crud_pacientes')
        except Exception as e:
            messages.error(request, f'Error al actualizar paciente: {e}')
    return render(request, 'editar_paciente.html', {'paciente': paciente})

def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        try:
            paciente.delete()
            messages.success(request, 'Paciente eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar paciente: {e}')
        return redirect('crud:crud_pacientes')
    return render(request, 'eliminar_paciente.html', {'paciente': paciente})

# ========== MÉDICOS ==========
def crud_medicos(request):
    medicos = Medico.objects.select_related('especialidad').all()
    q = request.GET.get('q', '')
    especialidad = request.GET.get('especialidad', '')
    if q:
        medicos = medicos.filter(Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(rut__icontains=q))
    if especialidad:
        medicos = medicos.filter(especialidad__id=especialidad)
    especialidades = Especialidad.objects.all()
    return render(request, 'crud_medicos.html', {'medicos': medicos, 'especialidades': especialidades})

def crear_medico(request):
    if request.method == 'POST':
        try:
            esp_id = request.POST.get('especialidad')
            esp = get_object_or_404(Especialidad, id=esp_id) if esp_id else None
            Medico.objects.create(
                rut=request.POST.get('rut', '').strip(),
                nombre=request.POST.get('nombre', '').strip(),
                apellido=request.POST.get('apellido', '').strip(),
                telefono=request.POST.get('telefono', '').strip(),
                correo=request.POST.get('correo', '').strip(),
                especialidad=esp
            )
            messages.success(request, 'Médico creado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear médico: {e}')
        return redirect('crud:crud_medicos')
    especialidades = Especialidad.objects.all()
    return render(request, 'crear_medico.html', {'especialidades': especialidades})

def editar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        try:
            medico.rut = request.POST.get('rut', medico.rut)
            medico.nombre = request.POST.get('nombre', medico.nombre)
            medico.apellido = request.POST.get('apellido', medico.apellido)
            medico.telefono = request.POST.get('telefono', medico.telefono)
            medico.correo = request.POST.get('correo', medico.correo)
            esp_id = request.POST.get('especialidad')
            medico.especialidad = get_object_or_404(Especialidad, id=esp_id) if esp_id else None
            medico.save()
            messages.success(request, 'Médico actualizado exitosamente!')
            return redirect('crud:crud_medicos')
        except Exception as e:
            messages.error(request, f'Error al actualizar médico: {e}')
    especialidades = Especialidad.objects.all()
    return render(request, 'editar_medico.html', {'medico': medico, 'especialidades': especialidades})

def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        try:
            medico.delete()
            messages.success(request, 'Médico eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar médico: {e}')
        return redirect('crud:crud_medicos')
    return render(request, 'eliminar_medico.html', {'medico': medico})

# ========== ESPECIALIDADES ==========
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
                raise ValueError('Nombre de especialidad requerido.')
            Especialidad.objects.create(nombre=nombre, descripcion=descripcion)
            messages.success(request, 'Especialidad creada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear especialidad: {e}')
        return redirect('crud:crud_especialidades')
    return render(request, 'crear_especialidad.html')

def editar_especialidad(request, id):
    esp = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        try:
            esp.nombre = request.POST.get('nombre', esp.nombre)
            esp.descripcion = request.POST.get('descripcion', esp.descripcion)
            esp.save()
            messages.success(request, 'Especialidad actualizada!')
            return redirect('crud:crud_especialidades')
        except Exception as e:
            messages.error(request, f'Error al actualizar especialidad: {e}')
    return render(request, 'editar_especialidad.html', {'especialidad': esp})

def eliminar_especialidad(request, id):
    esp = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        try:
            esp.delete()
            messages.success(request, 'Especialidad eliminada!')
        except Exception as e:
            messages.error(request, f'Error al eliminar especialidad: {e}')
        return redirect('crud:crud_especialidades')
    return render(request, 'eliminar_especialidad.html', {'especialidad': esp})

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
                nombre=request.POST.get('nombre', '').strip(),
                laboratorio=request.POST.get('laboratorio', '').strip(),
                descripcion=request.POST.get('descripcion', '').strip(),
                precio=precio
            )
            messages.success(request, 'Medicamento creado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear medicamento: {e}')
        return redirect('crud:crud_medicamentos')
    return render(request, 'crear_medicamento.html')

def editar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        try:
            medicamento.nombre = request.POST.get('nombre', medicamento.nombre)
            medicamento.laboratorio = request.POST.get('laboratorio', medicamento.laboratorio)
            medicamento.descripcion = request.POST.get('descripcion', medicamento.descripcion)
            precio_raw = request.POST.get('precio', '')
            if precio_raw != '':
                medicamento.precio = float(precio_raw)
            medicamento.save()
            messages.success(request, 'Medicamento actualizado exitosamente!')
            return redirect('crud:crud_medicamentos')
        except Exception as e:
            messages.error(request, f'Error al actualizar medicamento: {e}')
    return render(request, 'editar_medicamento.html', {'medicamento': medicamento})

def eliminar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        try:
            medicamento.delete()
            messages.success(request, 'Medicamento eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar medicamento: {e}')
        return redirect('crud:crud_medicamentos')
    return render(request, 'eliminar_medicamento.html', {'medicamento': medicamento})

# ========== TRATAMIENTOS / RECETAS ==========
def crud_tratamientos(request):
    tratamientos = Tratamiento.objects.all()
    return render(request, 'crud_tratamientos.html', {'tratamientos': tratamientos})

def crud_recetas(request):
    recetas = RecetaMedica.objects.all()
    return render(request, 'crud_recetas.html', {'recetas': recetas})

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
                nombre=request.POST.get('nombre', '').strip(),
                descripcion=request.POST.get('descripcion', '').strip(),
                capacidad=capacidad
            )
            messages.success(request, 'Sala creada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear sala: {e}')
        return redirect('crud:crud_salas')
    return render(request, 'crear_sala.html')

def editar_sala(request, id):
    sala = get_object_or_404(SalaAtencion, id=id)
    if request.method == 'POST':
        try:
            sala.nombre = request.POST.get('nombre', sala.nombre)
            sala.descripcion = request.POST.get('descripcion', sala.descripcion)
            capacidad_raw = request.POST.get('capacidad', '')
            if capacidad_raw != '':
                sala.capacidad = int(capacidad_raw)
            sala.save()
            messages.success(request, 'Sala actualizada!')
            return redirect('crud:crud_salas')
        except Exception as e:
            messages.error(request, f'Error al actualizar sala: {e}')
    return render(request, 'editar_sala.html', {'sala': sala})

def eliminar_sala(request, id):
    sala = get_object_or_404(SalaAtencion, id=id)
    if request.method == 'POST':
        try:
            sala.delete()
            messages.success(request, 'Sala eliminada!')
        except Exception as e:
            messages.error(request, f'Error al eliminar sala: {e}')
        return redirect('crud:crud_salas')
    return render(request, 'eliminar_sala.html', {'sala': sala})