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