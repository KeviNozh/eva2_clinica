"""
Formularios para el sistema Salud Vital
"""
from django import forms
from .models import Paciente, Medico, Medicamento, Especialidad, Sala, Tratamiento, Receta, Consulta, SeguimientoPaciente

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nombre', 'capacidad', 'tipo', 'descripcion', 'disponible']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción de la sala...'}),
        }

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['rut', 'nombre', 'apellido', 'fecha_nacimiento', 'genero', 'tipo_sangre', 'telefono', 'correo', 'direccion', 'activo']

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['rut', 'nombre', 'apellido', 'especialidad', 'telefono', 'correo']

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'laboratorio', 'descripcion', 'precio_unitario', 'stock', 'tipo']

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'fecha', 'sala', 'motivo', 'diagnostico', 'estado']

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['consulta', 'descripcion', 'fecha_inicio', 'fecha_fin', 'instrucciones']

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['consulta', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'instrucciones']

class SeguimientoPacienteForm(forms.ModelForm):
    class Meta:
        model = SeguimientoPaciente
        fields = ['paciente', 'medico', 'fecha_seguimiento', 'observaciones', 'proxima_cita', 'peso', 'altura', 'presion_arterial', 'temperatura']