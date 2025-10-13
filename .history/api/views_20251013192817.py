"""
VISTAS PARA LA API DEL SISTEMA SALUD VITAL
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
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class SalaAtencionViewSet(viewsets.ModelViewSet):
    queryset = SalaAtencion.objects.all()
    serializer_class = SalaAtencionSerializer

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'apellido', 'rut']
    filterset_class = MedicoFilter

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'apellido', 'rut']
    filterset_class = PacienteFilter

class ConsultaMedicaViewSet(viewsets.ModelViewSet):
    queryset = ConsultaMedica.objects.all()
    serializer_class = ConsultaMedicaSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['motivo', 'diagnostico']
    filterset_class = ConsultaMedicaFilter

class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer

class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

class RecetaMedicaViewSet(viewsets.ModelViewSet):
    queryset = RecetaMedica.objects.all()
    serializer_class = RecetaMedicaSerializer