"""
Formularios para el CRUD del sistema Salud Vital
Formularios Django para crear y editar registros
"""
from django import forms
from django.contrib.auth.models import User
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

class MedicoForm(forms.ModelForm):
    # Campos adicionales para el User
    rut = forms.CharField(
        max_length=12, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678-9',
            'required': True
        }),
        label='RUT *'
    )
    nombre = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Carlos',
            'required': True
        }),
        label='Nombre *'
    )
    apellido = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'López',
            'required': True
        }),
        label='Apellido *'
    )
    correo = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'doctor@clinica.cl'
        }),
        label='Correo Electrónico'
    )
    
    class Meta:
        model = Medico
        fields = ['especialidad', 'telefono']
        widgets = {
            'especialidad': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
        }
        labels = {
            'especialidad': 'Especialidad *',
            'telefono': 'Teléfono'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si estamos editando, cargar los datos del User
            self.fields['rut'].initial = self.instance.user.username
            self.fields['nombre'].initial = self.instance.user.first_name
            self.fields['apellido'].initial = self.instance.user.last_name
            self.fields['correo'].initial = self.instance.user.email

    def save(self, commit=True):
        medico = super().save(commit=False)
        
        # Crear o actualizar el User
        if self.instance.pk:
            # Edición
            user = medico.user
            user.first_name = self.cleaned_data['nombre']
            user.last_name = self.cleaned_data['apellido']
            user.email = self.cleaned_data['correo']
            if commit:
                user.save()
                medico.save()
        else:
            # Creación
            username = self.cleaned_data['rut'].replace('.', '').replace('-', '').lower()
            user = User.objects.create_user(
                username=username,
                password='temp123',  # Contraseña temporal
                first_name=self.cleaned_data['nombre'],
                last_name=self.cleaned_data['apellido'],
                email=self.cleaned_data['correo']
            )
            medico.user = user
            if commit:
                medico.save()
        
        return medico
        
class MedicamentoForm(forms.ModelForm):
    """Formulario para medicamentos"""
    class Meta:
        model = Medicamento
        fields = ['nombre', 'laboratorio', 'descripcion', 'precio_unitario', 'stock', 'tipo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class EspecialidadForm(forms.ModelForm):
    """Formulario para especialidades - CORREGIDO"""
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']  # ← Ambos campos incluidos
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cardiología, Pediatría, etc.',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la especialidad...',
                'rows': 3
            }),
        }

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