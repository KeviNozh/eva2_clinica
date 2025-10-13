"""
MODELOS DEL SISTEMA SALUD VITAL
Definición de entidades para gestión de pacientes, médicos y atenciones médicas
"""
from django.db import models

class Especialidad(models.Model):
    """
    Modelo para especialidades médicas
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"

    def __str__(self):
        return self.nombre


class SalaAtencion(models.Model):
    """
    MEJORA 1: Nueva tabla para gestión de salas de atención
    """
    TIPO_SALA_CHOICES = [
        ('Consulta General', 'Consulta General'),
        ('Emergencia', 'Emergencia'),
        ('Especialidad', 'Especialidad'),
        ('Procedimiento', 'Procedimiento'),
    ]
    
    numero_sala = models.IntegerField(unique=True)
    piso = models.IntegerField()
    tipo_sala = models.CharField(max_length=50, choices=TIPO_SALA_CHOICES)
    disponibilidad = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sala de Atención"
        verbose_name_plural = "Salas de Atención"

    def __str__(self):
        return f"Sala {self.numero_sala} - Piso {self.piso}"


class Medico(models.Model):
    """
    Modelo para médicos de la clínica
    """
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    activo = models.BooleanField(default=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido}"


class Paciente(models.Model):
    """
    Modelo para pacientes de la clínica
    """
    # MEJORA 2: Uso de CHOICES para género
    GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro'),
    ]
    
    TIPO_SANGRE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_CHOICES)
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class ConsultaMedica(models.Model):
    """
    Modelo para consultas médicas
    """
    ESTADO_CHOICES = [
        ('Programada', 'Programada'),
        ('Realizada', 'Realizada'),
        ('Cancelada', 'Cancelada'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    sala = models.ForeignKey(SalaAtencion, on_delete=models.CASCADE, null=True, blank=True)
    fecha_consulta = models.DateTimeField()
    motivo = models.TextField()
    diagnostico = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Programada')

    class Meta:
        verbose_name = "Consulta Médica"
        verbose_name_plural = "Consultas Médicas"

    def __str__(self):
        return f"Consulta {self.paciente} - {self.medico}"


class Tratamiento(models.Model):
    """
    Modelo para tratamientos médicos
    """
    consulta = models.ForeignKey(ConsultaMedica, on_delete=models.CASCADE)
    descripcion = models.TextField()
    duracion_dias = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"

    def __str__(self):
        return f"Tratamiento - {self.consulta}"


class Medicamento(models.Model):
    """
    Modelo para medicamentos
    """
    TIPO_MEDICAMENTO_CHOICES = [
        ('Tableta', 'Tableta'),
        ('Jarabe', 'Jarabe'),
        ('Inyección', 'Inyección'),
        ('Otro', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=100)
    laboratorio = models.CharField(max_length=100, blank=True, null=True)
    stock = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50, choices=TIPO_MEDICAMENTO_CHOICES, default='Tableta')

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"

    def __str__(self):
        return self.nombre


class RecetaMedica(models.Model):
    """
    Modelo para recetas médicas
    """
    consulta = models.ForeignKey(ConsultaMedica, on_delete=models.CASCADE)
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    fecha_emision = models.DateField(auto_now_add=True)
    indicaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Receta Médica"
        verbose_name_plural = "Recetas Médicas"

    def __str__(self):
        return f"Receta {self.consulta} - {self.medicamento}"