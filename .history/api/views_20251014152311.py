"""
Vistas para la API del sistema Salud Vital
Endpoints REST para todos los modelos
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
from .models import Sala

# Formularios
class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nombre', 'capacidad', 'tipo', 'descripcion', 'disponible']

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

# VISTAS CRUD PARA SALAS
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

# Otras vistas CRUD (manteniendo las que ya funcionan)
def crear_especialidad(request):
    if request.method == 'POST':
        try:
            Especialidad.objects.create(
                nombre=request.POST['nombre'],
                descripcion=request.POST.get('descripcion', '')
            )
            messages.success(request, "✅ Especialidad creada exitosamente!")
            return redirect('crud_especialidades')
        except Exception as e:
            messages.error(request, f"❌ Error al crear especialidad: {str(e)}")
    return render(request, 'crear_especialidad.html')

def lista_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'crud_especialidades.html', {'especialidades': especialidades})

# ... (mantener el resto de tus vistas CRUD existentes)