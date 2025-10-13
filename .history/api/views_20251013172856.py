"""
VISTAS PARA LA API DEL SISTEMA SALUD VITAL
Endpoints REST para todas las entidades del sistema
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (Especialidad, SalaAtencion, Medico, Paciente, 
                    ConsultaMedica, Tratamiento, Medicamento, RecetaMedica)
from .serializers import (EspecialidadSerializer, SalaAtencionSerializer, MedicoSerializer, 
                         PacienteSerializer, ConsultaMedicaSerializer, TratamientoSerializer, 
                         MedicamentoSerializer, RecetaMedicaSerializer)
from .filters import MedicoFilter, PacienteFilter, ConsultaMedicaFilter

class EspecialidadViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de especialidades médicas
    """
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'descripcion']

class SalaAtencionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de salas de atención
    """
    queryset = SalaAtencion.objects.all()
    serializer_class = SalaAtencionSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['numero_sala', 'tipo_sala']
    filterset_fields = ['piso', 'tipo_sala', 'disponibilidad']

class MedicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de médicos
    """
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'apellido', 'rut', 'especialidad__nombre']
    filterset_class = MedicoFilter

class PacienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de pacientes
    """
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'apellido', 'rut', 'correo']
    filterset_class = PacienteFilter

class ConsultaMedicaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de consultas médicas
    """
    queryset = ConsultaMedica.objects.all()
    serializer_class = ConsultaMedicaSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['motivo', 'diagnostico', 'medico__nombre', 'paciente__nombre']
    filterset_class = ConsultaMedicaFilter

class TratamientoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de tratamientos
    """
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['descripcion', 'observaciones']

class MedicamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de medicamentos
    """
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'laboratorio']
    filterset_fields = ['tipo']

class RecetaMedicaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de recetas médicas
    """
    queryset = RecetaMedica.objects.all()
    serializer_class = RecetaMedicaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['dosis', 'frecuencia', 'indicaciones']