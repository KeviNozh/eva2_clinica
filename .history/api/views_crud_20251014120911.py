# api/views_crud.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Paciente, Medico, Medicamento, Consulta, Receta, Tratamiento, Sala, Especialidad
from .forms import PacienteForm, MedicoForm, MedicamentoForm, EspecialidadForm, SalaForm, TratamientoForm, RecetaForm, ConsultaForm

# ========== VISTAS CRUD PRINCIPALES ==========

def crud_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'crud_pacientes.html', {'pacientes': pacientes})

def crud_medicos(request):
    medicos = Medico.objects.all()
    return render(request, 'crud_medicos.html', {'medicos': medicos})

def crud_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'crud_medicamentos.html', {'medicamentos': medicamentos})

def crud_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'crud_especialidades.html', {'especialidades': especialidades})

def crud_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'crud_consultas.html', {'consultas': consultas})

def crud_recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'crud_recetas.html', {'recetas': recetas})

def crud_tratamientos(request):
    tratamientos = Tratamiento.objects.all()
    return render(request, 'crud_tratamientos.html', {'tratamientos': tratamientos})

def crud_salas(request):
    salas = Sala.objects.all()
    return render(request, 'crud_salas.html', {'salas': salas})

# ========== CREAR ==========

def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'crear_paciente.html', {'form': form})

def crear_medico(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_medicos')
    else:
        form = MedicoForm()
    return render(request, 'crear_medico.html', {'form': form})

def crear_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_medicamentos')
    else:
        form = MedicamentoForm()
    return render(request, 'crear_medicamento.html', {'form': form})

def crear_especialidad(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_especialidades')
    else:
        form = EspecialidadForm()
    return render(request, 'crear_especialidad.html', {'form': form})

def crear_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_salas')
    else:
        form = SalaForm()
    return render(request, 'crear_sala.html', {'form': form})

def crear_tratamiento(request):
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_tratamientos')
    else:
        form = TratamientoForm()
    return render(request, 'crear_tratamiento.html', {'form': form})

def crear_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_recetas')
    else:
        form = RecetaForm()
    return render(request, 'crear_receta.html', {'form': form})

def crear_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_consultas')
    else:
        form = ConsultaForm()
    return render(request, 'crear_consulta.html', {'form': form})

# ========== EDITAR ==========

def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'editar_paciente.html', {'form': form, 'paciente': paciente})

def editar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_medicos')
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'editar_medico.html', {'form': form, 'medico': medico})

def editar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_medicamentos')
    else:
        form = MedicamentoForm(instance=medicamento)
    return render(request, 'editar_medicamento.html', {'form': form, 'medicamento': medicamento})

def editar_especialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_especialidades')
    else:
        form = EspecialidadForm(instance=especialidad)
    return render(request, 'editar_especialidad.html', {'form': form, 'especialidad': especialidad})

def editar_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_salas')
    else:
        form = SalaForm(instance=sala)
    return render(request, 'editar_sala.html', {'form': form, 'sala': sala})

def editar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_tratamientos')
    else:
        form = TratamientoForm(instance=tratamiento)
    return render(request, 'editar_tratamiento.html', {'form': form, 'tratamiento': tratamiento})

def editar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    if request.method == 'POST':
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_recetas')
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'editar_receta.html', {'form': form, 'receta': receta})

# ========== ELIMINAR ==========

def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('crud:crud_pacientes')
    return render(request, 'eliminar_paciente.html', {'paciente': paciente})

def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        medico.delete()
        return redirect('crud:crud_medicos')
    return render(request, 'eliminar_medico.html', {'medico': medico})

def eliminar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        medicamento.delete()
        return redirect('crud:crud_medicamentos')
    return render(request, 'eliminar_medicamento.html', {'medicamento': medicamento})

def eliminar_especialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        especialidad.delete()
        return redirect('crud:crud_especialidades')
    return render(request, 'eliminar_especialidad.html', {'especialidad': especialidad})

def eliminar_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        sala.delete()
        return redirect('crud:crud_salas')
    return render(request, 'eliminar_sala.html', {'sala': sala})

def eliminar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    if request.method == 'POST':
        tratamiento.delete()
        return redirect('crud:crud_tratamientos')
    return render(request, 'eliminar_tratamiento.html', {'tratamiento': tratamiento})

def eliminar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    if request.method == 'POST':
        receta.delete()
        return redirect('crud:crud_recetas')
    return render(request, 'eliminar_receta.html', {'receta': receta})