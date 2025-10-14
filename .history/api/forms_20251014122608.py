# api/forms.py
from django import forms
from .models import Paciente, Medico, Medicamento, Especialidad, SalaAtencion, Tratamiento, RecetaMedica, ConsultaMedica
# api/filters.py
import django_filters
from .models import Medico, Paciente, Consulta

class MedicoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    apellido = django_filters.CharFilter(field_name='user__last_name', lookup_expr='icontains')
    
    class Meta:
        model = Medico
        fields = ['especialidad']

class PacienteFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    apellido = django_filters.CharFilter(field_name='user__last_name', lookup_expr='icontains')
    telefono = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Paciente
        fields = ['telefono']

class ConsultaFilter(django_filters.FilterSet):  # Cambiado de ConsultaMedicaFilter
    paciente = django_filters.CharFilter(field_name='paciente__user__first_name', lookup_expr='icontains')
    medico = django_filters.CharFilter(field_name='medico__user__first_name', lookup_expr='icontains')
    
    class Meta:
        model = Consulta  # Cambiado de ConsultaMedica
        fields = ['fecha', 'sala']
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['user', 'fecha_nacimiento', 'telefono', 'direccion', 'alergias']

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['user', 'especialidad', 'telefono', 'direccion']

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'descripcion', 'precio', 'stock']

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre']

class SalaForm(forms.ModelForm):
    class Meta:
        model = SalaAtencion  # Actualizado
        fields = ['nombre', 'numero', 'piso', 'capacidad']

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = ConsultaMedica  # Actualizado
        fields = ['paciente', 'medico', 'fecha', 'sala', 'motivo', 'diagnostico']

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['consulta', 'descripcion', 'fecha_inicio', 'fecha_fin']

class RecetaForm(forms.ModelForm):
    class Meta:
        model = RecetaMedica  # Actualizado
        fields = ['consulta', 'medicamento', 'dosis', 'frecuencia', 'duracion']