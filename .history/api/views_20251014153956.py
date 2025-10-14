"""
Vistas para la API del sistema Salud Vital
Endpoints REST y CRUD completos para todos los modelos
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Especialidad, Sala, Medico, Paciente, Consulta, Medicamento, Tratamiento, Receta, SeguimientoPaciente
from .serializers import (
    EspecialidadSerializer, SalaSerializer, MedicoSerializer, 
    PacienteSerializer, ConsultaSerializer, MedicamentoSerializer,
    TratamientoSerializer, RecetaSerializer, SeguimientoPacienteSerializer
)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django import forms
from .models import Sala, Especialidad, Medico, Paciente, Consulta, Medicamento, Tratamiento, Receta, SeguimientoPaciente

# FORMULARIOS COMPLETOS
class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nombre', 'capacidad', 'tipo', 'descripcion', 'disponible']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la sala...'}),
        }

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la especialidad...'}),
        }

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['rut', 'nombre', 'apellido', 'especialidad', 'telefono', 'correo']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['rut', 'nombre', 'apellido', 'fecha_nacimiento', 'genero', 'tipo_sangre', 'telefono', 'correo', 'direccion', 'activo']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'laboratorio', 'descripcion', 'precio_unitario', 'stock', 'tipo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
        }

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'fecha', 'sala', 'motivo', 'diagnostico', 'estado']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
        }

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['consulta', 'descripcion', 'fecha_inicio', 'fecha_fin', 'instrucciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'instrucciones': forms.Textarea(attrs={'rows': 2}),
        }

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['consulta', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'instrucciones']
        widgets = {
            'instrucciones': forms.Textarea(attrs={'rows': 2}),
        }

class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = SeguimientoPaciente
        fields = ['paciente', 'medico', 'fecha_seguimiento', 'observaciones', 'proxima_cita', 'peso', 'altura', 'presion_arterial', 'temperatura']
        widgets = {
            'fecha_seguimiento': forms.DateInput(attrs={'type': 'date'}),
            'proxima_cita': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

# VISTAS API (ViewSets)
class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre']

class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre', 'tipo']

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre', 'apellido', 'especialidad__nombre']

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'apellido', 'rut']

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer

class RecetaViewSet(viewsets.ModelViewSet):
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer

class SeguimientoPacienteViewSet(viewsets.ModelViewSet):
    queryset = SeguimientoPaciente.objects.all()
    serializer_class = SeguimientoPacienteSerializer

# VISTAS CRUD COMPLETAS PARA TODOS LOS MODELOS

# ESPECIALIDADES
def crear_especialidad(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Especialidad creada exitosamente!")
            return redirect('crud_especialidades')
    else:
        form = EspecialidadForm()
    return render(request, 'crear_especialidad.html', {'form': form})

def lista_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'crud_especialidades.html', {'especialidades': especialidades})

def editar_especialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Especialidad actualizada exitosamente!")
            return redirect('crud_especialidades')
    else:
        form = EspecialidadForm(instance=especialidad)
    return render(request, 'editar_especialidad.html', {'form': form})

def eliminar_especialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        especialidad.delete()
        messages.success(request, "✅ Especialidad eliminada exitosamente!")
        return redirect('crud_especialidades')
    return render(request, 'eliminar_especialidad.html', {'especialidad': especialidad})

# SALAS
def crear_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Sala creada exitosamente!")
            return redirect('crud_salas')
    else:
        form = SalaForm()
    return render(request, 'crear_sala.html', {'form': form})

def lista_salas(request):
    salas = Sala.objects.all()
    return render(request, 'crud_salas.html', {'salas': salas})

def editar_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Sala actualizada exitosamente!")
            return redirect('crud_salas')
    else:
        form = SalaForm(instance=sala)
    return render(request, 'editar_sala.html', {'form': form})

def eliminar_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        sala.delete()
        messages.success(request, "✅ Sala eliminada exitosamente!")
        return redirect('crud_salas')
    return render(request, 'eliminar_sala.html', {'sala': sala})

# MÉDICOS
def crear_medico(request):
    especialidades = Especialidad.objects.all()
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Médico creado exitosamente!")
            return redirect('crud_medicos')
    else:
        form = MedicoForm()
    return render(request, 'crear_medico.html', {'form': form, 'especialidades': especialidades})

def lista_medicos(request):
    medicos = Medico.objects.all()
    return render(request, 'crud_medicos.html', {'medicos': medicos})

def editar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    especialidades = Especialidad.objects.all()
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Médico actualizado exitosamente!")
            return redirect('crud_medicos')
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'editar_medico.html', {'form': form, 'especialidades': especialidades})

def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        medico.delete()
        messages.success(request, "✅ Médico eliminado exitosamente!")
        return redirect('crud_medicos')
    return render(request, 'eliminar_medico.html', {'medico': medico})

# PACIENTES
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Paciente creado exitosamente!")
            return redirect('crud_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'crear_paciente.html', {'form': form})

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'crud_pacientes.html', {'pacientes': pacientes})

def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Paciente actualizado exitosamente!")
            return redirect('crud_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'editar_paciente.html', {'form': form})

def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, "✅ Paciente eliminado exitosamente!")
        return redirect('crud_pacientes')
    return render(request, 'eliminar_paciente.html', {'paciente': paciente})

# MEDICAMENTOS
def crear_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Medicamento creado exitosamente!")
            return redirect('crud_medicamentos')
    else:
        form = MedicamentoForm()
    return render(request, 'crear_medicamento.html', {'form': form})

def lista_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'crud_medicamentos.html', {'medicamentos': medicamentos})

def editar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Medicamento actualizado exitosamente!")
            return redirect('crud_medicamentos')
    else:
        form = MedicamentoForm(instance=medicamento)
    return render(request, 'editar_medicamento.html', {'form': form})

def eliminar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        medicamento.delete()
        messages.success(request, "✅ Medicamento eliminado exitosamente!")
        return redirect('crud_medicamentos')
    return render(request, 'eliminar_medicamento.html', {'medicamento': medicamento})

# CONSULTAS
def crear_consulta(request):
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    salas = Sala.objects.all()
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Consulta creada exitosamente!")
            return redirect('crud_consultas')
    else:
        form = ConsultaForm()
    
    return render(request, 'crear_consulta.html', {
        'form': form,
        'pacientes': pacientes,
        'medicos': medicos,
        'salas': salas
    })

def lista_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'crud_consultas.html', {'consultas': consultas})

def editar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    salas = Sala.objects.all()
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Consulta actualizada exitosamente!")
            return redirect('crud_consultas')
    else:
        form = ConsultaForm(instance=consulta)
    
    return render(request, 'editar_consulta.html', {
        'form': form,
        'pacientes': pacientes,
        'medicos': medicos,
        'salas': salas
    })

def eliminar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, "✅ Consulta eliminada exitosamente!")
        return redirect('crud_consultas')
    return render(request, 'eliminar_consulta.html', {'consulta': consulta})

# TRATAMIENTOS
def crear_tratamiento(request):
    consultas = Consulta.objects.all()
    
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Tratamiento creado exitosamente!")
            return redirect('crud_tratamientos')
    else:
        form = TratamientoForm()
    
    return render(request, 'crear_tratamiento.html', {'form': form, 'consultas': consultas})

def lista_tratamientos(request):
    tratamientos = Tratamiento.objects.all()
    return render(request, 'crud_tratamientos.html', {'tratamientos': tratamientos})

def editar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    consultas = Consulta.objects.all()
    
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Tratamiento actualizado exitosamente!")
            return redirect('crud_tratamientos')
    else:
        form = TratamientoForm(instance=tratamiento)
    
    return render(request, 'editar_tratamiento.html', {'form': form, 'consultas': consultas})

def eliminar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    if request.method == 'POST':
        tratamiento.delete()
        messages.success(request, "✅ Tratamiento eliminado exitosamente!")
        return redirect('crud_tratamientos')
    return render(request, 'eliminar_tratamiento.html', {'tratamiento': tratamiento})

# RECETAS
def crear_receta(request):
    consultas = Consulta.objects.all()
    medicamentos = Medicamento.objects.all()
    
    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Receta creada exitosamente!")
            return redirect('crud_recetas')
    else:
        form = RecetaForm()
    
    return render(request, 'crear_receta.html', {'form': form, 'consultas': consultas, 'medicamentos': medicamentos})

def lista_recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'crud_recetas.html', {'recetas': recetas})

def editar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    consultas = Consulta.objects.all()
    medicamentos = Medicamento.objects.all()
    
    if request.method == 'POST':
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Receta actualizada exitosamente!")
            return redirect('crud_recetas')
    else:
        form = RecetaForm(instance=receta)
    
    return render(request, 'editar_receta.html', {'form': form, 'consultas': consultas, 'medicamentos': medicamentos})

def eliminar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    if request.method == 'POST':
        receta.delete()
        messages.success(request, "✅ Receta eliminada exitosamente!")
        return redirect('crud_recetas')
    return render(request, 'eliminar_receta.html', {'receta': receta})

# SEGUIMIENTOS
def crear_seguimiento(request):
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    
    if request.method == 'POST':
        form = SeguimientoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Seguimiento creado exitosamente!")
            return redirect('crud_seguimientos')
    else:
        form = SeguimientoForm()
    
    return render(request, 'crear_seguimiento.html', {'form': form, 'pacientes': pacientes, 'medicos': medicos})

def lista_seguimientos(request):
    seguimientos = SeguimientoPaciente.objects.all()
    return render(request, 'crud_seguimientos.html', {'seguimientos': seguimientos})

def editar_seguimiento(request, id):
    seguimiento = get_object_or_404(SeguimientoPaciente, id=id)
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    
    if request.method == 'POST':
        form = SeguimientoForm(request.POST, instance=seguimiento)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Seguimiento actualizado exitosamente!")
            return redirect('crud_seguimientos')
    else:
        form = SeguimientoForm(instance=seguimiento)
    
    return render(request, 'editar_seguimiento.html', {'form': form, 'pacientes': pacientes, 'medicos': medicos})

def eliminar_seguimiento(request, id):
    seguimiento = get_object_or_404(SeguimientoPaciente, id=id)
    if request.method == 'POST':
        seguimiento.delete()
        messages.success(request, "✅ Seguimiento eliminado exitosamente!")
        return redirect('crud_seguimientos')
    return render(request, 'eliminar_seguimiento.html', {'seguimiento': seguimiento})