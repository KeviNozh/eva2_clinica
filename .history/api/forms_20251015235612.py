"""
Formularios para el CRUD del sistema Salud Vital
Formularios Django para crear y editar registros
"""
from django import forms
from django.contrib.auth.models import User
from .models import Paciente, Medico, Medicamento, Especialidad, Sala, Tratamiento, Receta, Consulta, SeguimientoPaciente
from .models import Receta, Consulta, Medicamento
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control-custom'}),
            'rut': forms.TextInput(attrs={'class': 'form-control-custom'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control-custom'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control-custom'}),
            'genero': forms.Select(attrs={'class': 'form-select-custom'}),
            'tipo_sangre': forms.Select(attrs={'class': 'form-select-custom'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control-custom'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control-custom'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control-custom'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MedicoForm(forms.ModelForm):
    rut = forms.CharField(max_length=12, required=True, label="RUT")
    nombre = forms.CharField(max_length=100, required=True, label="Nombre")
    apellido = forms.CharField(max_length=100, required=True, label="Apellido")
    correo = forms.EmailField(required=False, label="Correo Electrónico")

    class Meta:
        model = Medico
        fields = ['especialidad', 'telefono']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['rut'].initial = self.instance.user.username
            self.fields['nombre'].initial = self.instance.user.first_name
            self.fields['apellido'].initial = self.instance.user.last_name
            self.fields['correo'].initial = self.instance.user.email
            self.fields['rut'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        medico = super().save(commit=False)
        rut = self.cleaned_data['rut']
        username = rut.replace('.', '').replace('-', '').lower()

        if self.instance and self.instance.pk:
            user = self.instance.user
            user.first_name = self.cleaned_data['nombre']
            user.last_name = self.cleaned_data['apellido']
            user.email = self.cleaned_data['correo']
            user.save()
        else:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Ya existe un usuario con este RUT.")
            user = User.objects.create_user(
                username=username,
                password='temp_password123', # Contraseña temporal
                first_name=self.cleaned_data['nombre'],
                last_name=self.cleaned_data['apellido'],
                email=self.cleaned_data['correo']
            )
            medico.user = user

        if commit:
            medico.save()
        return medico

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = '__all__'

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = '__all__'
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = '__all__'

class RecetaForm(forms.ModelForm):
    """Formulario para Recetas, con estilos y widgets personalizados."""
    class Meta:
        model = Receta
        fields = ['consulta', 'medicamento', 'cantidad', 'dosis', 'frecuencia', 'duracion', 'instrucciones']
        
        # Aquí definimos cómo se debe ver cada campo
        widgets = {
            'consulta': forms.Select(attrs={'class': 'form-select-custom'}),
            'medicamento': forms.Select(attrs={'class': 'form-select-custom'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control-custom'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control-custom', 'placeholder': 'Ej: 500mg'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control-custom', 'placeholder': 'Ej: Cada 8 horas'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control-custom', 'placeholder': 'Ej: 7 días'}),
            'instrucciones': forms.Textarea(attrs={'class': 'form-control-custom', 'rows': 4, 'placeholder': 'Instrucciones adicionales para el paciente...'}),
        }
        
        # Etiquetas que se mostrarán en el formulario
        labels = {
            'consulta': 'Consulta *',
            'medicamento': 'Medicamento *',
            'cantidad': 'Cantidad *',
            'dosis': 'Dosis *',
            'frecuencia': 'Frecuencia *',
            'duracion': 'Duración *',
            'instrucciones': 'Instrucciones Especiales',
        }

    def __init__(self, *args, **kwargs):
        super(RecetaForm, self).__init__(*args, **kwargs)
        # Hacemos que las opciones de los menús desplegables se vean más amigables
        self.fields['consulta'].queryset = Consulta.objects.select_related('paciente', 'medico__user').all()
        self.fields['consulta'].label_from_instance = lambda obj: f"{obj.paciente.nombre} {obj.paciente.apellido} - Dr. {obj.medico.user.first_name} - {obj.fecha.strftime('%d/%m/%Y')}"
        
        self.fields['medicamento'].queryset = Medicamento.objects.all()
        self.fields['medicamento'].label_from_instance = lambda obj: f"{obj.nombre} - {obj.laboratorio}"
class SeguimientoPacienteForm(forms.ModelForm):
    class Meta:
        model = SeguimientoPaciente
        fields = '__all__'
        widgets = {
            'fecha_seguimiento': forms.DateInput(attrs={'type': 'date'}),
            'proxima_cita': forms.DateInput(attrs={'type': 'date'}),
        }