"""
Formularios para el CRUD del sistema Salud Vital
Formularios Django para crear y editar registros
"""
from django import forms
from .models import Paciente, Medico, Medicamento, Especialidad, Sala, Tratamiento, Receta, Consulta, SeguimientoPaciente

class PacienteForm(forms.ModelForm):
    """Formulario para pacientes"""
    class Meta:
        model = Paciente
        fields = ['rut', 'nombre', 'apellido', 'fecha_nacimiento', 'genero', 
                 'tipo_sangre', 'telefono', 'correo', 'direccion', 'activo']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

def crear_medico(request):
    especialidades = Especialidad.objects.all()
    print(f"Especialidades encontradas: {especialidades.count()}")  # Debug
    
    if request.method == 'POST':
        # ... resto del código
    else:
        form = MedicoForm()
    
    return render(request, 'crear_medico.html', {
        'form': form,
        'especialidades': especialidades
    })

class MedicamentoForm(forms.ModelForm):
    """Formulario para medicamentos"""
    class Meta:
        model = Medicamento
        fields = ['nombre', 'laboratorio', 'descripcion', 'precio_unitario', 'stock', 'tipo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class EspecialidadForm(forms.ModelForm):
    """Formulario para especialidades"""
    class Meta:
        model = Especialidad
        fields = ['nombre']

class SalaForm(forms.ModelForm):
    """Formulario para salas"""
    class Meta:
        model = Sala
        fields = ['nombre', 'numero', 'piso', 'capacidad']

class ConsultaForm(forms.ModelForm):
    """Formulario para consultas médicas"""
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'fecha', 'sala', 'motivo', 'diagnostico', 'estado']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
        }

class TratamientoForm(forms.ModelForm):
    """Formulario para tratamientos"""
    class Meta:
        model = Tratamiento
        fields = ['consulta', 'descripcion', 'fecha_inicio', 'fecha_fin', 'instrucciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'instrucciones': forms.Textarea(attrs={'rows': 3}),
        }

class RecetaForm(forms.ModelForm):
    """Formulario para recetas médicas"""
    class Meta:
        model = Receta
        fields = ['consulta', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'instrucciones']
        widgets = {
            'instrucciones': forms.Textarea(attrs={'rows': 3}),
        }

class SeguimientoPacienteForm(forms.ModelForm):
    """Formulario para seguimiento de pacientes"""
    class Meta:
        model = SeguimientoPaciente
        fields = ['paciente', 'medico', 'fecha_seguimiento', 'observaciones', 
                 'proxima_cita', 'peso', 'altura', 'presion_arterial', 'temperatura']
        widgets = {
            'fecha_seguimiento': forms.DateInput(attrs={'type': 'date'}),
            'proxima_cita': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 4}),
        }