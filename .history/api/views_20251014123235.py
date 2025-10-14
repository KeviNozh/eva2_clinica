# api/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Especialidad, Sala, Medico, Paciente, Consulta, Tratamiento, Medicamento, Receta
from .serializers import (EspecialidadSerializer, MedicoSerializer, 
                         PacienteSerializer, MedicamentoSerializer, 
                         TratamientoSerializer), SalaSerializer, ConsultaSerializer, RecetaSerializer
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

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer
    
    
class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

class RecetaViewSet(viewsets.ModelViewSet):  # Cambiado de RecetaMedicaViewSet
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer