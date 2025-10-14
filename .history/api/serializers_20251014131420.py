"""
Serializers para la API del sistema Salud Vital
Convierte modelos en JSON para la API REST
"""
from rest_framework import serializers
from .models import Especialidad, Medico, Paciente, Medicamento, Tratamiento, Sala, Consulta, Receta, SeguimientoPaciente

class EspecialidadSerializer(serializers.ModelSerializer):
    """Serializer para especialidades médicas"""
    class Meta:
        model = Especialidad
        fields = '__all__'

class SalaSerializer(serializers.ModelSerializer):
    """Serializer para salas de atención"""
    class Meta:
        model = Sala
        fields = '__all__'

class MedicoSerializer(serializers.ModelSerializer):
    """Serializer para médicos"""
    especialidad_nombre = serializers.CharField(source='especialidad.nombre', read_only=True)
    
    class Meta:
        model = Medico
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    """Serializer para pacientes"""
    class Meta:
        model = Paciente
        fields = '__all__'

class ConsultaSerializer(serializers.ModelSerializer):
    """Serializer para consultas médicas"""
    paciente_nombre = serializers.CharField(source='paciente.nombre', read_only=True)
    medico_nombre = serializers.CharField(source='medico.nombre', read_only=True)
    sala_numero = serializers.CharField(source='sala.numero', read_only=True)
    
    class Meta:
        model = Consulta
        fields = '__all__'

class MedicamentoSerializer(serializers.ModelSerializer):
    """Serializer para medicamentos"""
    class Meta:
        model = Medicamento
        fields = '__all__'

class TratamientoSerializer(serializers.ModelSerializer):
    """Serializer para tratamientos"""
    consulta_info = serializers.CharField(source='consulta.__str__', read_only=True)
    
    class Meta:
        model = Tratamiento
        fields = '__all__'

class RecetaSerializer(serializers.ModelSerializer):
    """Serializer para recetas médicas"""
    medicamento_nombre = serializers.CharField(source='medicamento.nombre', read_only=True)
    consulta_info = serializers.CharField(source='consulta.__str__', read_only=True)
    
    class Meta:
        model = Receta
        fields = '__all__'

class SeguimientoPacienteSerializer(serializers.ModelSerializer):
    """Serializer para seguimiento de pacientes"""
    paciente_nombre = serializers.CharField(source='paciente.nombre', read_only=True)
    medico_nombre = serializers.CharField(source='medico.nombre', read_only=True)
    
    class Meta:
        model = SeguimientoPaciente
        fields = '__all__'