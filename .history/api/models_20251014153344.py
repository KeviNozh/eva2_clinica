"""
Modelos del sistema Salud Vital
Define todas las entidades del sistema médico
"""
from django.db import models
from django.contrib.auth.models import User



class Especialidad(models.Model):
    """Modelo para especialidades médicas"""
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Sala(models.Model):
    """Modelo para salas de atención"""
    nombre = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    piso = models.IntegerField(default=1)  # Valor por defecto
    capacidad = models.IntegerField(default=5)  # Valor por defecto
    
    def __str__(self):
        return f"Sala {self.numero} - {self.nombre}"

class Medico(models.Model):
    """Modelo para médicos del sistema"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, default='')  # Campo opcional
    direccion = models.TextField(blank=True, default='')  # Campo opcional
    
    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

class Paciente(models.Model):
    """Modelo para pacientes del sistema"""
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
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
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='M')  # Valor por defecto
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_CHOICES, default='O+')  # Valor por defecto
    telefono = models.CharField(max_length=15, blank=True, default='')
    correo = models.EmailField(blank=True, default='')
    direccion = models.TextField(blank=True, default='')
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"

class Consulta(models.Model):
    """Modelo para consultas médicas"""
    ESTADO_CHOICES = [  # MEJORA 1: USO DE CHOICES
        ('programada', 'Programada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
        ('reprogramada', 'Reprogramada'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    motivo = models.TextField()
    diagnostico = models.TextField(blank=True, default='')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada')
    
    def __str__(self):
        return f"Consulta {self.id} - {self.paciente}"

class Medicamento(models.Model):
    """Modelo para medicamentos del inventario"""
    TIPO_CHOICES = [
        ('Tableta', 'Tableta'),
        ('Cápsula', 'Cápsula'),
        ('Jarabe', 'Jarabe'),
        ('Inyección', 'Inyección'),
        ('Crema', 'Crema'),
        ('Otro', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=100)
    laboratorio = models.CharField(max_length=100, blank=True, default='')
    descripcion = models.TextField(blank=True, default='')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Tableta')
    
    def __str__(self):
        return self.nombre

class Tratamiento(models.Model):
    """Modelo para tratamientos médicos"""
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    instrucciones = models.TextField(blank=True, default='')
    
    def __str__(self):
        return f"Tratamiento {self.id} - {self.consulta}"

class Receta(models.Model):
    """Modelo para recetas médicas"""
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    instrucciones = models.TextField(blank=True, default='')
    
    def __str__(self):
        return f"Receta {self.id} - {self.medicamento}"

class SeguimientoPaciente(models.Model):
    """MEJORA 2: NUEVA TABLA - Seguimiento de pacientes"""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_seguimiento = models.DateField()
    observaciones = models.TextField()
    proxima_cita = models.DateField(blank=True, null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    altura = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    presion_arterial = models.CharField(max_length=20, blank=True, default='')
    temperatura = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"Seguimiento {self.id} - {self.paciente}"