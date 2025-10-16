"""
Filtros para la API del sistema Salud Vital
Filtros avanzados para búsquedas específicas
"""
import django_filters
from .models import Medico, Paciente, Consulta, Medicamento

class MedicoFilter(django_filters.FilterSet):
    """Filtros para médicos"""
    nombre = django_filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    apellido = django_filters.CharFilter(field_name='user__last_name', lookup_expr='icontains')
    especialidad_nombre = django_filters.CharFilter(field_name='especialidad__nombre', lookup_expr='icontains')

    class Meta:
        model = Medico
        fields = []  # CORREGIDO: Se deja vacío o se elimina para evitar conflicto.

class PacienteFilter(django_filters.FilterSet):
    """Filtros para pacientes"""
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    apellido = django_filters.CharFilter(lookup_expr='icontains')
    rut = django_filters.CharFilter(lookup_expr='icontains')
    telefono = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Paciente
        fields = ['genero', 'tipo_sangre', 'activo']

class ConsultaFilter(django_filters.FilterSet):
    """Filtros para consultas"""
    paciente_nombre = django_filters.CharFilter(field_name='paciente__nombre', lookup_expr='icontains')
    medico_nombre = django_filters.CharFilter(field_name='medico__user__first_name', lookup_expr='icontains')
    fecha_desde = django_filters.DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha', lookup_expr='lte')

    class Meta:
        model = Consulta
        fields = ['estado', 'sala', 'medico']

class MedicamentoFilter(django_filters.FilterSet):
    """Filtros para medicamentos"""
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    laboratorio = django_filters.CharFilter(lookup_expr='icontains')
    precio_min = django_filters.NumberFilter(field_name='precio_unitario', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio_unitario', lookup_expr='lte')

    class Meta:
        model = Medicamento
        fields = ['tipo']