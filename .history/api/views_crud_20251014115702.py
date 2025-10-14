"""
VISTAS PARA LOS TEMPLATES CRUD - Funciones completas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import (Especialidad, SalaAtencion, Medico, Paciente,
                     ConsultaMedica, Tratamiento, Medicamento, RecetaMedica)

# ========== CONSULTAS ==========
def crud_consultas(request):
    consultas = ConsultaMedica.objects.select_related('paciente', 'medico').all()
    return render(request, 'crud_consultas.html', {'consultas': consultas})

# ========== MEDICAMENTOS ==========
def crud_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'crud_medicamentos.html', {'medicamentos': medicamentos})

def crear_medicamento(request):
    if request.method == 'POST':
        try:
            stock = int(request.POST.get('stock', 0))
            precio = float(request.POST.get('precio_unitario', 0))
            
            Medicamento.objects.create(
                nombre=request.POST.get('nombre', '').strip(),
                laboratorio=request.POST.get('laboratorio', '').strip(),
                stock=stock,
                precio_unitario=precio,
                tipo=request.POST.get('tipo', 'Tableta')
            )
            messages.success(request, 'Medicamento creado exitosamente!')
            return redirect('crud:crud_medicamentos')
        except Exception as e:
            messages.error(request, f'Error al crear medicamento: {str(e)}')
    
    return render(request, 'crear_medicamento.html')

def editar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    
    if request.method == 'POST':
        try:
            medicamento.nombre = request.POST.get('nombre', medicamento.nombre)
            medicamento.laboratorio = request.POST.get('laboratorio', medicamento.laboratorio)
            medicamento.stock = int(request.POST.get('stock', medicamento.stock))
            medicamento.precio_unitario = float(request.POST.get('precio_unitario', medicamento.precio_unitario))
            medicamento.tipo = request.POST.get('tipo', medicamento.tipo)
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

# ========== TRATAMIENTOS ==========
def crud_tratamientos(request):
    tratamientos = Tratamiento.objects.select_related('consulta').all()
    return render(request, 'crud_tratamientos.html', {'tratamientos': tratamientos})

def crear_tratamiento(request):
    if request.method == 'POST':
        try:
            consulta_id = request.POST.get('consulta')
            consulta = get_object_or_404(ConsultaMedica, id=consulta_id) if consulta_id else None
            
            Tratamiento.objects.create(
                consulta=consulta,
                descripcion=request.POST.get('descripcion', '').strip(),
                duracion_dias=int(request.POST.get('duracion_dias', 0)),
                observaciones=request.POST.get('observaciones', '').strip()
            )
            messages.success(request, 'Tratamiento creado exitosamente!')
            return redirect('crud:crud_tratamientos')
        except Exception as e:
            messages.error(request, f'Error al crear tratamiento: {str(e)}')
    
    consultas = ConsultaMedica.objects.all()
    return render(request, 'crear_tratamiento.html', {'consultas': consultas})

def editar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    
    if request.method == 'POST':
        try:
            consulta_id = request.POST.get('consulta')
            tratamiento.consulta = get_object_or_404(ConsultaMedica, id=consulta_id) if consulta_id else tratamiento.consulta
            tratamiento.descripcion = request.POST.get('descripcion', tratamiento.descripcion)
            tratamiento.duracion_dias = int(request.POST.get('duracion_dias', tratamiento.duracion_dias))
            tratamiento.observaciones = request.POST.get('observaciones', tratamiento.observaciones)
            tratamiento.save()
            
            messages.success(request, 'Tratamiento actualizado exitosamente!')
            return redirect('crud:crud_tratamientos')
        except Exception as e:
            messages.error(request, f'Error al actualizar tratamiento: {str(e)}')
    
    consultas = ConsultaMedica.objects.all()
    return render(request, 'editar_tratamiento.html', {'tratamiento': tratamiento, 'consultas': consultas})

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
    return render(request, 'crud_recetas.html', {'recetas': recetas})

def crear_receta(request):
    if request.method == 'POST':
        try:
            consulta_id = request.POST.get('consulta')
            medicamento_id = request.POST.get('medicamento')
            
            consulta = get_object_or_404(ConsultaMedica, id=consulta_id) if consulta_id else None
            medicamento = get_object_or_404(Medicamento, id=medicamento_id) if medicamento_id else None
            
            RecetaMedica.objects.create(
                consulta=consulta,
                medicamento=medicamento,
                dosis=request.POST.get('dosis', '').strip(),
                frecuencia=request.POST.get('frecuencia', '').strip(),
                duracion=request.POST.get('duracion', '').strip(),
                indicaciones=request.POST.get('indicaciones', '').strip()
            )
            messages.success(request, 'Receta creada exitosamente!')
            return redirect('crud:crud_recetas')
        except Exception as e:
            messages.error(request, f'Error al crear receta: {str(e)}')
    
    consultas = ConsultaMedica.objects.all()
    medicamentos = Medicamento.objects.all()
    return render(request, 'crear_receta.html', {
        'consultas': consultas,
        'medicamentos': medicamentos
    })

def editar_receta(request, id):
    receta = get_object_or_404(RecetaMedica, id=id)
    
    if request.method == 'POST':
        try:
            consulta_id = request.POST.get('consulta')
            medicamento_id = request.POST.get('medicamento')
            
            receta.consulta = get_object_or_404(ConsultaMedica, id=consulta_id) if consulta_id else receta.consulta
            receta.medicamento = get_object_or_404(Medicamento, id=medicamento_id) if medicamento_id else receta.medicamento
            receta.dosis = request.POST.get('dosis', receta.dosis)
            receta.frecuencia = request.POST.get('frecuencia', receta.frecuencia)
            receta.duracion = request.POST.get('duracion', receta.duracion)
            receta.indicaciones = request.POST.get('indicaciones', receta.indicaciones)
            receta.save()
            
            messages.success(request, 'Receta actualizada exitosamente!')
            return redirect('crud:crud_recetas')
        except Exception as e:
            messages.error(request, f'Error al actualizar receta: {str(e)}')
    
    consultas = ConsultaMedica.objects.all()
    medicamentos = Medicamento.objects.all()
    return render(request, 'editar_receta.html', {
        'receta': receta,
        'consultas': consultas,
        'medicamentos': medicamentos
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
                numero_sala=int(request.POST.get('numero_sala', 0)),
                piso=int(request.POST.get('piso', 1)),
                tipo_sala=request.POST.get('tipo_sala', 'Consulta General'),
                disponibilidad=request.POST.get('disponibilidad') == 'on'
            )
            messages.success(request, 'Sala creada exitosamente!')
            return redirect('crud:crud_salas')
        except Exception as e:
            messages.error(request, f'Error al crear sala: {str(e)}')
    
    return render(request, 'crear_sala.html')

def editar_sala(request, id):
    sala = get_object_or_404(SalaAtencion, id=id)
    
    if request.method == 'POST':
        try:
            sala.numero_sala = int(request.POST.get('numero_sala', sala.numero_sala))
            sala.piso = int(request.POST.get('piso', sala.piso))
            sala.tipo_sala = request.POST.get('tipo_sala', sala.tipo_sala)
            sala.disponibilidad = request.POST.get('disponibilidad') == 'on'
            sala.save()
            
            messages.success(request, 'Sala actualizada exitosamente!')
            return redirect('crud:crud_salas')
        except Exception as e:
            messages.error(request, f'Error al actualizar sala: {str(e)}')
    
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