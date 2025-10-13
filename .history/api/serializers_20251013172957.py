"""
SERIALIZERS PARA LA API DEL SISTEMA SALUD VITAL
Conversión de modelos a JSON para la API REST
"""
from rest_framework import serializers
from .models import (Especialidad, SalaAtencion, Medico, Paciente, 
                    ConsultaMedica, Tratamiento, Medicamento, RecetaMedica)

class EspecialidadSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Especialidad
    """
    class Meta:
        model = Especialidad
        fields = '__all__'

class SalaAtencionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SalaAtencion
    """
    class Meta:
        model = SalaAtencion
        fields = '__all__'

class MedicoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Medico
    """
    especialidad_nombre = serializers.CharField(source='especialidad.nombre', read_only=True)
    
    class Meta:
        model = Medico
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Paciente
    """
    class Meta:
        model = Paciente
        fields = '__all__'

class ConsultaMedicaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ConsultaMedica
    """
    paciente_nombre = serializers.CharField(source='paciente.nombre', read_only=True)
    medico_nombre = serializers.CharField(source='medico.nombre', read_only=True)
    sala_numero = serializers.IntegerField(source='sala.numero_sala', read_only=True)
    
    class Meta:
        model = ConsultaMedica
        fields = '__all__'

class TratamientoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Tratamiento
    """
    consulta_info = serializers.CharField(source='consulta.motivo', read_only=True)
    
    class Meta:
        model = Tratamiento
        fields = '__all__'

class MedicamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Medicamento
    """
    class Meta:
        model = Medicamento
        fields = '__all__'

class RecetaMedicaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo RecetaMedica
    """
    consulta_info = serializers.CharField(source='consulta.motivo', read_only=True)
    tratamiento_info = serializers.CharField(source='tratamiento.descripcion', read_only=True)
    medicamento_nombre = serializers.CharField(source='medicamento.nombre', read_only=True)
    
    class Meta:
        model = RecetaMedica
        fields = '__all__'