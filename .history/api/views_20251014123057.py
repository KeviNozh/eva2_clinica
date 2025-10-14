# api/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Especialidad, Sala, Medico, Paciente, Consulta, Tratamiento, Medicamento, Receta
from .serializers import (EspecialidadSerializer, SalaSerializer, MedicoSerializer,
                         PacienteSerializer, ConsultaSerializer, TratamientoSerializer,
                         MedicamentoSerializer, RecetaSerializer)
from .filters import MedicoFilter, PacienteFilter, ConsultaFilter
# api/views.py - MÍNIMA
# api/views.py
from rest_framework import viewsets
from django.http import HttpResponse
import json

# Vistas básicas para que funcione
class EspecialidadViewSet(viewsets.ModelViewSet):
    pass

class MedicoViewSet(viewsets.ModelViewSet):
    pass

class PacienteViewSet(viewsets.ModelViewSet):
    pass

class TratamientoViewSet(viewsets.ModelViewSet):
    pass

class MedicamentoViewSet(viewsets.ModelViewSet):
    pass

# Vista de inicio temporal
def api_home(request):
    return HttpResponse(json.dumps({"message": "API funcionando"}), content_type="application/json")    
class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class SalaViewSet(viewsets.ModelViewSet):  # Cambiado de SalaAtencionViewSet
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MedicoFilter
    search_fields = ['user__first_name', 'user__last_name']

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PacienteFilter
    search_fields = ['user__first_name', 'user__last_name']

class ConsultaViewSet(viewsets.ModelViewSet):  # Cambiado de ConsultaMedicaViewSet
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ConsultaFilter

class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer

class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

class RecetaViewSet(viewsets.ModelViewSet):  # Cambiado de RecetaMedicaViewSet
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer