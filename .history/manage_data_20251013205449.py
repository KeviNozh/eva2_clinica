"""
SCRIPT PARA CARGAR DATOS DE PRUEBA REALISTAS
"""
import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_vital.settings')
django.setup()

from api.models import (Especialidad, SalaAtencion, Medico, Paciente, 
                       ConsultaMedica, Tratamiento, Medicamento, RecetaMedica)

def cargar_datos():
    print("Cargando datos de prueba...")
    
    # Limpiar datos existentes
    RecetaMedica.objects.all().delete()
    Tratamiento.objects.all().delete()
    ConsultaMedica.objects.all().delete()
    Medicamento.objects.all().delete()
    Medico.objects.all().delete()
    Paciente.objects.all().delete()
    SalaAtencion.objects.all().delete()
    Especialidad.objects.all().delete()
    
    # 1. Especialidades
    especialidades_data = [
        {'nombre': 'Cardiología', 'descripcion': 'Especialidad en enfermedades del corazón'},
        {'nombre': 'Pediatría', 'descripcion': 'Especialidad en atención infantil'},
        {'nombre': 'Dermatología', 'descripcion': 'Especialidad en enfermedades de la piel'},
        {'nombre': 'Ginecología', 'descripcion': 'Especialidad en salud femenina'},
        {'nombre': 'Traumatología', 'descripcion': 'Especialidad en huesos y articulaciones'},
    ]
    
    especialidades = []
    for esp in especialidades_data:
        especialidad = Especialidad.objects.create(**esp)
        especialidades.append(especialidad)
        print(f'Especialidad creada: {especialidad.nombre}')
    
    # 2. Salas de atención
    salas_data = [
        {'numero_sala': 101, 'piso': 1, 'tipo_sala': 'Consulta General', 'disponibilidad': True},
        {'numero_sala': 102, 'piso': 1, 'tipo_sala': 'Consulta General', 'disponibilidad': True},
        {'numero_sala': 201, 'piso': 2, 'tipo_sala': 'Emergencia', 'disponibilidad': False},
        {'numero_sala': 202, 'piso': 2, 'tipo_sala': 'Especialidad', 'disponibilidad': True},
        {'numero_sala': 301, 'piso': 3, 'tipo_sala': 'Procedimiento', 'disponibilidad': True},
    ]
    
    salas = []
    for sala in salas_data:
        sala_obj = SalaAtencion.objects.create(**sala)
        salas.append(sala_obj)
        print(f'Sala creada: {sala_obj}')
    
    # 3. Médicos
    medicos_data = [
        {'rut': '12345678-9', 'nombre': 'Carlos', 'apellido': 'López', 'especialidad': especialidades[0]},
        {'rut': '23456789-0', 'nombre': 'Ana', 'apellido': 'Martínez', 'especialidad': especialidades[1]},
        {'rut': '34567890-1', 'nombre': 'Roberto', 'apellido': 'García', 'especialidad': especialidades[2]},
        {'rut': '45678901-2', 'nombre': 'María', 'apellido': 'Rodríguez', 'especialidad': especialidades[3]},
        {'rut': '56789012-3', 'nombre': 'Pedro', 'apellido': 'Fernández', 'especialidad': especialidades[4]},
    ]
    
    medicos = []
    for med in medicos_data:
        medico = Medico.objects.create(
            rut=med['rut'],
            nombre=med['nombre'],
            apellido=med['apellido'],
            correo=f"{med['nombre'].lower()}.{med['apellido'].lower()}@clinicavital.cl",
            telefono=f"+569{random.randint(10000000, 99999999)}",
            especialidad=med['especialidad'],
            activo=True
        )
        medicos.append(medico)
        print(f'Médico creado: {medico}')
    
    # 4. Pacientes
    pacientes_data = [
        {'rut': '98765432-1', 'nombre': 'Juan', 'apellido': 'Pérez', 'fecha_nacimiento': '1985-03-15', 'genero': 'Masculino', 'tipo_sangre': 'A+'},
        {'rut': '87654321-2', 'nombre': 'Laura', 'apellido': 'González', 'fecha_nacimiento': '1990-07-22', 'genero': 'Femenino', 'tipo_sangre': 'O+'},
        {'rut': '76543210-3', 'nombre': 'Diego', 'apellido': 'Silva', 'fecha_nacimiento': '1978-11-30', 'genero': 'Masculino', 'tipo_sangre': 'B+'},
        {'rut': '65432109-4', 'nombre': 'Camila', 'apellido': 'Rojas', 'fecha_nacimiento': '1995-05-10', 'genero': 'Femenino', 'tipo_sangre': 'AB+'},
        {'rut': '54321098-5', 'nombre': 'Andrés', 'apellido': 'Mendoza', 'fecha_nacimiento': '1982-12-05', 'genero': 'Masculino', 'tipo_sangre': 'A-'},
    ]
    
    pacientes = []
    for pac in pacientes_data:
        paciente = Paciente.objects.create(
            rut=pac['rut'],
            nombre=pac['nombre'],
            apellido=pac['apellido'],
            fecha_nacimiento=pac['fecha_nacimiento'],
            genero=pac['genero'],
            tipo_sangre=pac['tipo_sangre'],
            correo=f"{pac['nombre'].lower()}.{pac['apellido'].lower()}@gmail.com",
            telefono=f"+569{random.randint(10000000, 99999999)}",
            direccion=f"Calle {random.randint(1, 1000)} #123",
            activo=True
        )
        pacientes.append(paciente)
        print(f'Paciente creado: {paciente}')
    
    # 5. Medicamentos
    medicamentos_data = [
        {'nombre': 'Paracetamol', 'laboratorio': 'Bayer', 'stock': 100, 'precio_unitario': 1500, 'tipo': 'Tableta'},
        {'nombre': 'Ibuprofeno', 'laboratorio': 'Pfizer', 'stock': 80, 'precio_unitario': 1200, 'tipo': 'Tableta'},
        {'nombre': 'Amoxicilina', 'laboratorio': 'Roche', 'stock': 50, 'precio_unitario': 3500, 'tipo': 'Tableta'},
        {'nombre': 'Jarabe para la tos', 'laboratorio': 'Johnson & Johnson', 'stock': 30, 'precio_unitario': 4500, 'tipo': 'Jarabe'},
        {'nombre': 'Insulina', 'laboratorio': 'Novo Nordisk', 'stock': 20, 'precio_unitario': 12000, 'tipo': 'Inyección'},
    ]
    
    medicamentos = []
    for med in medicamentos_data:
        medicamento = Medicamento.objects.create(**med)
        medicamentos.append(medicamento)
        print(f'Medicamento creado: {medicamento.nombre}')
    
    # 6. Consultas médicas
    consultas = []
    for i in range(10):
        consulta = ConsultaMedica.objects.create(
            paciente=random.choice(pacientes),
            medico=random.choice(medicos),
            sala=random.choice(salas),
            fecha_consulta=datetime.now() - timedelta(days=random.randint(1, 30)),
            motivo=f"Consulta por {random.choice(['dolor de cabeza', 'fiebre', 'dolor abdominal', 'control rutinario', 'seguimiento'])}",
            diagnostico=random.choice(['Gripe común', 'Infección respiratoria', 'Gastritis', 'Hipertensión', 'Diabetes']),
            estado=random.choice(['Programada', 'Realizada', 'Cancelada'])
        )
        consultas.append(consulta)
        print(f'Consulta creada: {consulta}')
    
    # 7. Tratamientos
    tratamientos = []
    for consulta in consultas:
        if consulta.estado == 'Realizada':
            tratamiento = Tratamiento.objects.create(
                consulta=consulta,
                descripcion=f"Tratamiento para {consulta.diagnostico}",
                duracion_dias=random.randint(7, 30),
                observaciones="Seguir las indicaciones al pie de la letra"
            )
            tratamientos.append(tratamiento)
            print(f'Tratamiento creado: {tratamiento}')
    
    # 8. Recetas médicas
    for tratamiento in tratamientos:
        receta = RecetaMedica.objects.create(
            consulta=tratamiento.consulta,
            tratamiento=tratamiento,
            medicamento=random.choice(medicamentos),
            dosis=random.choice(['1 tableta', '2 tabletas', '5 ml', '10 ml']),
            frecuencia=random.choice(['Cada 8 horas', 'Cada 12 horas', 'Una vez al día', 'Cada 6 horas']),
            duracion=f"{random.randint(5, 15)} días",
            indicaciones="Tomar con alimentos"
        )
        print(f'Receta creada: {receta}')
    
    print("¡Datos de prueba cargados exitosamente!")

if __name__ == '__main__':
    cargar_datos()