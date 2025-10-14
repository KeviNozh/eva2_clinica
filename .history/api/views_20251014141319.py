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
from .filters import MedicoFilter, PacienteFilter, ConsultaFilter
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Paciente
from .forms import PacienteForm  
# Agrega estas vistas NORMALES para formularios HTML
def crear_paciente_view(request):
    """Vista normal para formulario HTML de crear paciente"""
    if request.method == 'POST':
        try:
            # Crear paciente con los datos del formulario
            paciente = Paciente(
                rut=request.POST['rut'],
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                fecha_nacimiento=request.POST['fecha_nacimiento'],
                genero=request.POST['genero'],
                tipo_sangre=request.POST['tipo_sangre'],
                telefono=request.POST.get('telefono', ''),
                correo=request.POST.get('correo', ''),
                direccion=request.POST.get('direccion', '')
            )
            paciente.save()
            messages.success(request, "Paciente creado exitosamente!")
            return redirect('lista_pacientes')  # Cambia por tu URL
            
        except Exception as e:
            messages.error(request, f"Error al crear paciente: {str(e)}")
    
    return render(request, 'crear_paciente.html')
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'crear_paciente.html', {'form': form})

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'lista_pacientes.html', {'pacientes': pacientes})
def lista_pacientes_view(request):
    """Vista normal para listar pacientes"""
    pacientes = Paciente.objects.filter(activo=True)
    return render(request, 'lista_pacientes.html', {'pacientes': pacientes})
class EspecialidadViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar especialidades médicas"""
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre']

class SalaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar salas de atención"""
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre', 'numero']
    filterset_fields = ['piso']

class MedicoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar médicos"""
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'especialidad__nombre']
    filterset_fields = ['especialidad']

class PacienteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar pacientes"""
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'apellido', 'rut', 'correo']
    filterset_fields = ['genero', 'tipo_sangre', 'activo']
    ordering_fields = ['fecha_registro', 'nombre', 'apellido']

class ConsultaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar consultas médicas"""
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paciente__nombre', 'medico__user__first_name', 'motivo']
    filterset_fields = ['estado', 'sala', 'medico']
    ordering_fields = ['fecha']

class MedicamentoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar medicamentos"""
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre', 'laboratorio']
    filterset_fields = ['tipo']

class TratamientoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar tratamientos"""
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['descripcion', 'consulta__paciente__nombre']

class RecetaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar recetas médicas"""
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['medicamento__nombre', 'consulta__paciente__nombre']

class SeguimientoPacienteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar seguimiento de pacientes"""
    queryset = SeguimientoPaciente.objects.all()
    serializer_class = SeguimientoPacienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paciente__nombre', 'medico__user__first_name', 'observaciones']
    filterset_fields = ['paciente', 'medico']
    ordering_fields = ['fecha_seguimiento']

