"""
VISTAS PARA LOS TEMPLATES CRUD - Conexión real con PostgreSQL
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import (Especialidad, SalaAtencion, Medico, Paciente, 
                    ConsultaMedica, Tratamiento, Medicamento, RecetaMedica)
from django.db import models

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

def editar_especialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        try:
            especialidad.nombre = request.POST['nombre']
            especialidad.descripcion = request.POST.get('descripcion', '')
            especialidad.save()
            messages.success(request, 'Especialidad actualizada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al actualizar especialidad: {str(e)}')
        return redirect('crud:crud_especialidades')
    
    return render(request, 'editar_especialidad.html', {'especialidad': especialidad})

def eliminar_especialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        try:
            especialidad.delete()
            messages.success(request, 'Especialidad eliminada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar especialidad: {str(e)}')
        return redirect('crud:crud_especialidades')
    
    return render(request, 'eliminar_especialidad.html', {'especialidad': especialidad})

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

def editar_consulta(request, id):
    consulta = get_object_or_404(ConsultaMedica, id=id)
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    salas = SalaAtencion.objects.all()
    
    if request.method == 'POST':
        try:
            consulta.paciente = Paciente.objects.get(id=request.POST['paciente'])
            consulta.medico = Medico.objects.get(id=request.POST['medico'])
            consulta.sala = SalaAtencion.objects.get(id=request.POST['sala']) if request.POST.get('sala') else None
            consulta.fecha_consulta = request.POST['fecha_consulta']
            consulta.motivo = request.POST['motivo']
            consulta.diagnostico = request.POST.get('diagnostico', '')
            consulta.estado = request.POST.get('estado', 'Programada')
            consulta.save()
            messages.success(request, 'Consulta actualizada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al actualizar consulta: {str(e)}')
        return redirect('crud:crud_consultas')
    
    return render(request, 'editar_consulta.html', {
        'consulta': consulta,
        'pacientes': pacientes,
        'medicos': medicos,
        'salas': salas
    })

def eliminar_consulta(request, id):
    consulta = get_object_or_404(ConsultaMedica, id=id)
    if request.method == 'POST':
        try:
            consulta.delete()
            messages.success(request, 'Consulta eliminada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar consulta: {str(e)}')
        return redirect('crud:crud_consultas')
    
    return render(request, 'eliminar_consulta.html', {'consulta': consulta})

# ========== MEDICAMENTOS ==========
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
    return redirect('crud:crud_medicamentos')

def editar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        try:
            medicamento.nombre = request.POST['nombre']
            medicamento.laboratorio = request.POST.get('laboratorio', '')
            medicamento.stock = request.POST.get('stock', 0)
            medicamento.precio_unitario = request.POST.get('precio_unitario', 0)
            medicamento.tipo = request.POST.get('tipo', 'Tableta')
            medicamento.save()
            messages.success(request, 'Medicamento actualizado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al actualizar medicamento: {str(e)}')
        return redirect('crud:crud_medicamentos')
    
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

# ========== TRATAMIENTOS ==========
def crud_tratamientos(request):
    tratamientos = Tratamiento.objects.select_related('consulta').all()
    consultas = ConsultaMedica.objects.all()
    return render(request, 'crud_tratamientos.html', {
        'tratamientos': tratamientos,
        'consultas': consultas
    })

def crear_tratamiento(request):
    if request.method == 'POST':
        try:
            consulta = ConsultaMedica.objects.get(id=request.POST['consulta'])
            Tratamiento.objects.create(
                consulta=consulta,
                descripcion=request.POST['descripcion'],
                duracion_dias=request.POST['duracion_dias'],
                observaciones=request.POST.get('observaciones', '')
            )
            messages.success(request, 'Tratamiento creado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear tratamiento: {str(e)}')
    return redirect('crud:crud_tratamientos')

def editar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    consultas = ConsultaMedica.objects.all()
    
    if request.method == 'POST':
        try:
            tratamiento.consulta = ConsultaMedica.objects.get(id=request.POST['consulta'])
            tratamiento.descripcion = request.POST['descripcion']
            tratamiento.duracion_dias = request.POST['duracion_dias']
            tratamiento.observaciones = request.POST.get('observaciones', '')
            tratamiento.save()
            messages.success(request, 'Tratamiento actualizado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al actualizar tratamiento: {str(e)}')
        return redirect('crud:crud_tratamientos')
    
    return render(request, 'editar_tratamiento.html', {
        'tratamiento': tratamiento,
        'consultas': consultas
    })

def eliminar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    if request.method == 'POST':
        try:
            tratamiento.delete()
            messages.success(request, 'Tratamiento eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar tratamiento: {str(e)}')
        return redirect('crud:crud_tratamientos')
    
    return render(request, 'eliminar_tratamiento.html', {'tratamiento': tratamiento})

# ========== RECETAS ==========
def crud_recetas(request):
    recetas = RecetaMedica.objects.select_related('consulta', 'medicamento').all()
    consultas = ConsultaMedica.objects.all()
    medicamentos = Medicamento.objects.all()
    tratamientos = Tratamiento.objects.all()
    return render(request, 'crud_recetas.html', {
        'recetas': recetas,
        'consultas': consultas,
        'medicamentos': medicamentos,
        'tratamientos': tratamientos
    })

def crear_receta(request):
    if request.method == 'POST':
        try:
            consulta = ConsultaMedica.objects.get(id=request.POST['consulta'])
            medicamento = Medicamento.objects.get(id=request.POST['medicamento'])
            tratamiento = Tratamiento.objects.get(id=request.POST['tratamiento'])
            
            RecetaMedica.objects.create(
                consulta=consulta,
                medicamento=medicamento,
                tratamiento=tratamiento,
                dosis=request.POST['dosis'],
                frecuencia=request.POST['frecuencia'],
                duracion=request.POST['duracion'],
                indicaciones=request.POST.get('indicaciones', '')
            )
            messages.success(request, 'Receta creada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al crear receta: {str(e)}')
    return redirect('crud:crud_recetas')

def editar_receta(request, id):
    receta = get_object_or_404(RecetaMedica, id=id)
    consultas = ConsultaMedica.objects.all()
    medicamentos = Medicamento.objects.all()
    tratamientos = Tratamiento.objects.all()
    
    if request.method == 'POST':
        try:
            receta.consulta = ConsultaMedica.objects.get(id=request.POST['consulta'])
            receta.medicamento = Medicamento.objects.get(id=request.POST['medicamento'])
            receta.tratamiento = Tratamiento.objects.get(id=request.POST['tratamiento'])
            receta.dosis = request.POST['dosis']
            receta.frecuencia = request.POST['frecuencia']
            receta.duracion = request.POST['duracion']
            receta.indicaciones = request.POST.get('indicaciones', '')
            receta.save()
            messages.success(request, 'Receta actualizada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al actualizar receta: {str(e)}')
        return redirect('crud:crud_recetas')
    
    return render(request, 'editar_receta.html', {
        'receta': receta,
        'consultas': consultas,
        'medicamentos': medicamentos,
        'tratamientos': tratamientos
    })

def eliminar_receta(request, id):
    receta = get_object_or_404(RecetaMedica, id=id)
    if request.method == 'POST':
        try:
            receta.delete()
            messages.success(request, 'Receta eliminada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar receta: {str(e)}')
        return redirect('crud:crud_recetas')
    
    return render(request, 'eliminar_receta.html', {'receta': receta})

# ========== SALAS ==========
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
    return redirect('crud:crud_salas')

def editar_sala(request, id):
    sala = get_object_or_404(SalaAtencion, id=id)
    if request.method == 'POST':
        try:
            sala.numero_sala = request.POST['numero_sala']
            sala.piso = request.POST['piso']
            sala.tipo_sala = request.POST['tipo_sala']
            sala.disponibilidad = request.POST.get('disponibilidad', True)
            sala.save()
            messages.success(request, 'Sala actualizada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al actualizar sala: {str(e)}')
        return redirect('crud:crud_salas')
    
    return render(request, 'editar_sala.html', {'sala': sala})

def eliminar_sala(request, id):
    sala = get_object_or_404(SalaAtencion, id=id)
    if request.method == 'POST':
        try:
            sala.delete()
            messages.success(request, 'Sala eliminada exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar sala: {str(e)}')
        return redirect('crud:crud_salas')
    
    return render(request, 'eliminar_sala.html', {'sala': sala})