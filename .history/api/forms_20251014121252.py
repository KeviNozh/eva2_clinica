# api/forms.py
from django import forms
from .models import Paciente, Medico, Medicamento, Especialidad, Sala, Tratamiento, Receta, Consulta

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
        model = Sala
        fields = ['nombre', 'numero', 'piso', 'capacidad']

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'fecha', 'sala', 'motivo', 'diagnostico']

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['consulta', 'descripcion', 'fecha_inicio', 'fecha_fin']

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['consulta', 'medicamento', 'dosis', 'frecuencia', 'duracion']