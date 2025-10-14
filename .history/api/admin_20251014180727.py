"""
Configuración del admin para el sistema Salud Vital
"""
from django.contrib import admin
from .models import Especialidad, Sala, Medico, Paciente, Consulta, Medicamento, Tratamiento, Receta, SeguimientoPaciente

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    """Admin para especialidades"""
    list_display = ['id', 'nombre']
    search_fields = ['nombre']

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    """Admin para salas"""
    list_display = ['id', 'nombre', 'numero', 'piso', 'capacidad']
    list_filter = ['piso']
    search_fields = ['nombre', 'numero']

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    """Admin para médicos"""
    list_display = ['id', 'user', 'especialidad', 'telefono']
    list_filter = ['especialidad']
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    """Admin para pacientes"""
    list_display = ['id', 'rut', 'nombre', 'apellido', 'genero', 'tipo_sangre', 'activo']
    list_filter = ['genero', 'tipo_sangre', 'activo']
    search_fields = ['nombre', 'apellido', 'rut']

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    """Admin para consultas"""
    list_display = ['id', 'paciente', 'medico', 'fecha', 'estado']
    list_filter = ['estado', 'sala', 'fecha']
    search_fields = ['paciente__nombre', 'medico__user__first_name']

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    """Admin para medicamentos"""
    list_display = ['id', 'nombre', 'laboratorio', 'precio_unitario', 'stock', 'tipo']
    list_filter = ['tipo']
    search_fields = ['nombre', 'laboratorio']

@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    """Admin para tratamientos"""
    # Usa SOLO los campos que existen en tu modelo Tratamiento
    list_display = ['id', 'consulta', 'medicamento', 'dosis', 'duracion', 'fecha_creacion']
    list_filter = ['consulta', 'fecha_creacion']
    search_fields = ['medicamento', 'consulta__paciente__nombre', 'consulta__paciente__apellido']

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    """Admin para recetas"""
    list_display = ['id', 'consulta', 'medicamento', 'dosis']
    search_fields = ['consulta__paciente__nombre', 'medicamento__nombre']

@admin.register(SeguimientoPaciente)
class SeguimientoPacienteAdmin(admin.ModelAdmin):
    """Admin para seguimientos de pacientes"""
    list_display = ['id', 'paciente', 'medico', 'fecha_seguimiento', 'proxima_cita']
    list_filter = ['fecha_seguimiento']
    search_fields = ['paciente__nombre', 'medico__user__first_name']