"""
Vistas CRUD para el sistema Salud Vital
Vistas basadas en funciones para los templates
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Paciente, Medico, Medicamento, Consulta, Receta, Tratamiento, Sala, Especialidad, SeguimientoPaciente
from .forms import PacienteForm, MedicoForm, MedicamentoForm, EspecialidadForm, SalaForm, TratamientoForm, RecetaForm, ConsultaForm, SeguimientoPacienteForm

# ========== VISTAS CRUD PRINCIPALES ==========

def crud_pacientes(request):
    """Vista para listar pacientes"""
    pacientes = Paciente.objects.all()
    
    # Filtros
    query = request.GET.get('q', '')
    genero = request.GET.get('genero', '')
    tipo_sangre = request.GET.get('tipo_sangre', '')
    activo = request.GET.get('activo', '')
    
    if query:
        pacientes = pacientes.filter(
            models.Q(nombre__icontains=query) | 
            models.Q(apellido__icontains=query) |
            models.Q(rut__icontains=query)
        )
    
    if genero:
        pacientes = pacientes.filter(genero=genero)
    
    if tipo_sangre:
        pacientes = pacientes.filter(tipo_sangre=tipo_sangre)
    
    if activo:
        pacientes = pacientes.filter(activo=activo == 'true')
    
    return render(request, 'crud_pacientes.html', {'pacientes': pacientes})

def crud_medicos(request):
    """Vista para listar médicos"""
    medicos = Medico.objects.all()
    especialidades = Especialidad.objects.all()
    
    # Filtros
    query = request.GET.get('q', '')
    especialidad_id = request.GET.get('especialidad', '')
    
    if query:
        medicos = medicos.filter(
            models.Q(user__first_name__icontains=query) | 
            models.Q(user__last_name__icontains=query)
        )
    
    if especialidad_id:
        medicos = medicos.filter(especialidad_id=especialidad_id)
    
    return render(request, 'crud_medicos.html', {
        'medicos': medicos,
        'especialidades': especialidades
    })

def crud_medicamentos(request):
    """Vista para listar medicamentos"""
    medicamentos = Medicamento.objects.all()
    return render(request, 'crud_medicamentos.html', {'medicamentos': medicamentos})

def crud_especialidades(request):
    """Vista para listar especialidades"""
    especialidades = Especialidad.objects.all()
    return render(request, 'crud_especialidades.html', {'especialidades': especialidades})

def crud_consultas(request):
    """Vista para listar consultas"""
    consultas = Consulta.objects.all()
    return render(request, 'crud_consultas.html', {'consultas': consultas})

def crud_recetas(request):
    """Vista para listar recetas"""
    recetas = Receta.objects.all()
    return render(request, 'crud_recetas.html', {'recetas': recetas})

def crud_tratamientos(request):
    """Vista para listar tratamientos"""
    tratamientos = Tratamiento.objects.all()
    return render(request, 'crud_tratamientos.html', {'tratamientos': tratamientos})

def crud_salas(request):
    """Vista para listar salas"""
    salas = Sala.objects.all()
    return render(request, 'crud_salas.html', {'salas': salas})

def crud_seguimientos(request):
    """Vista para listar seguimientos de pacientes"""
    seguimientos = SeguimientoPaciente.objects.all()
    return render(request, 'crud_seguimientos.html', {'seguimientos': seguimientos})

# ========== CREAR ==========

def crear_paciente(request):
    """Vista para crear paciente"""
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente creado exitosamente!')
            return redirect('crud:crud_pacientes')
        else:
            messages.error(request, 'Error al crear el paciente. Verifique los datos.')
    else:
        form = PacienteForm()
    
    return render(request, 'crear_paciente.html', {'form': form})

def crear_medico(request):
    """Vista para crear médico"""
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médico creado exitosamente!')
            return redirect('crud:crud_medicos')
        else:
            messages.error(request, 'Error al crear el médico. Verifique los datos.')
    else:
        form = MedicoForm()
    
    return render(request, 'crear_medico.html', {'form': form})

def crear_medicamento(request):
    """Vista para crear medicamento"""
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicamento creado exitosamente!')
            return redirect('crud:crud_medicamentos')
        else:
            messages.error(request, 'Error al crear el medicamento. Verifique los datos.')
    else:
        form = MedicamentoForm()
    
    return render(request, 'crear_medicamento.html', {'form': form})

def crear_especialidad(request):
    """Vista para crear especialidad"""
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialidad creada exitosamente!')
            return redirect('crud:crud_especialidades')
        else:
            messages.error(request, 'Error al crear la especialidad. Verifique los datos.')
    else:
        form = EspecialidadForm()
    
    return render(request, 'crear_especialidad.html', {'form': form})

def crear_sala(request):
    """Vista para crear sala"""
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sala creada exitosamente!')
            return redirect('crud:crud_salas')
        else:
            messages.error(request, 'Error al crear la sala. Verifique los datos.')
    else:
        form = SalaForm()
    
    return render(request, 'crear_sala.html', {'form': form})

def crear_consulta(request):
    """Vista para crear consulta"""
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta creada exitosamente!')
            return redirect('crud:crud_consultas')
        else:
            messages.error(request, 'Error al crear la consulta. Verifique los datos.')
    else:
        form = ConsultaForm()
    
    return render(request, 'crear_consulta.html', {'form': form})

def crear_tratamiento(request):
    """Vista para crear tratamiento"""
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tratamiento creado exitosamente!')
            return redirect('crud:crud_tratamientos')
        else:
            messages.error(request, 'Error al crear el tratamiento. Verifique los datos.')
    else:
        form = TratamientoForm()
    
    return render(request, 'crear_tratamiento.html', {'form': form})

def crear_receta(request):
    """Vista para crear receta"""
    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receta creada exitosamente!')
            return redirect('crud:crud_recetas')
        else:
            messages.error(request, 'Error al crear la receta. Verifique los datos.')
    else:
        form = RecetaForm()
    
    return render(request, 'crear_receta.html', {'form': form})

def crear_seguimiento(request):
    """Vista para crear seguimiento"""
    if request.method == 'POST':
        form = SeguimientoPacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seguimiento creado exitosamente!')
            return redirect('crud:crud_seguimientos')
        else:
            messages.error(request, 'Error al crear el seguimiento. Verifique los datos.')
    else:
        form = SeguimientoPacienteForm()
    
    return render(request, 'crear_seguimiento.html', {'form': form})

# ========== EDITAR ==========

def editar_paciente(request, id):
    """Vista para editar paciente"""
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado exitosamente!')
            return redirect('crud:crud_pacientes')
        else:
            messages.error(request, 'Error al actualizar el paciente. Verifique los datos.')
    else:
        form = PacienteForm(instance=paciente)
    
    return render(request, 'editar_paciente.html', {'form': form, 'paciente': paciente})

def editar_medico(request, id):
    """Vista para editar médico"""
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médico actualizado exitosamente!')
            return redirect('crud:crud_medicos')
        else:
            messages.error(request, 'Error al actualizar el médico. Verifique los datos.')
    else:
        form = MedicoForm(instance=medico)
    
    return render(request, 'editar_medico.html', {'form': form, 'medico': medico})

def editar_medicamento(request, id):
    """Vista para editar medicamento"""
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicamento actualizado exitosamente!')
            return redirect('crud:crud_medicamentos')
        else:
            messages.error(request, 'Error al actualizar el medicamento. Verifique los datos.')
    else:
        form = MedicamentoForm(instance=medicamento)
    
    return render(request, 'editar_medicamento.html', {'form': form, 'medicamento': medicamento})

# ========== ELIMINAR ==========

def eliminar_paciente(request, id):
    """Vista para eliminar paciente"""
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Paciente eliminado exitosamente!')
        return redirect('crud:crud_pacientes')
    
    return render(request, 'eliminar_paciente.html', {'paciente': paciente})

def eliminar_medico(request, id):
    """Vista para eliminar médico"""
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        medico.delete()
        messages.success(request, 'Médico eliminado exitosamente!')
        return redirect('crud:crud_medicos')
    
    return render(request, 'eliminar_medico.html', {'medico': medico})

def eliminar_medicamento(request, id):
    """Vista para eliminar medicamento"""
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        medicamento.delete()
        messages.success(request, 'Medicamento eliminado exitosamente!')
        return redirect('crud:crud_medicamentos')
    
    return render(request, 'eliminar_medicamento.html', {'medicamento': medicamento})