"""
FILTROS PARA LA API DEL SISTEMA SALUD VITAL
Sistema de filtrado para búsquedas específicas
"""
import django_filters
from .models import Medico, Paciente, ConsultaMedica

class MedicoFilter(django_filters.FilterSet):
    """
    Filtros para médicos por especialidad y estado
    """
    especialidad = django_filters.CharFilter(field_name='especialidad__nombre', lookup_expr='icontains')
    activo = django_filters.BooleanFilter(field_name='activo')
    
    class Meta:
        model = Medico
        fields = ['especialidad', 'activo']

class PacienteFilter(django_filters.FilterSet):
    """
    Filtros para pacientes por género y tipo de sangre
    """
    genero = django_filters.ChoiceFilter(choices=Paciente.GENERO_CHOICES)
    tipo_sangre = django_filters.ChoiceFilter(choices=Paciente.TIPO_SANGRE_CHOICES)
    activo = django_filters.BooleanFilter(field_name='activo')
    
    class Meta:
        model = Paciente
        fields = ['genero', 'tipo_sangre', 'activo']

class ConsultaMedicaFilter(django_filters.FilterSet):
    """
    Filtros para consultas médicas por médico, paciente y estado
    """
    medico = django_filters.CharFilter(field_name='medico__nombre', lookup_expr='icontains')
    paciente = django_filters.CharFilter(field_name='paciente__nombre', lookup_expr='icontains')
    estado = django_filters.ChoiceFilter(choices=ConsultaMedica.ESTADO_CHOICES)
    fecha_consulta = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = ConsultaMedica
        fields = ['medico', 'paciente', 'estado', 'fecha_consulta']