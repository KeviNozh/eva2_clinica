"""
SCRIPT PARA CARGAR DATOS DE PRUEBA REALISTAS
Sistema Salud Vital - Evaluación 2
"""
import os
import django
import random
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_vital.settings')
django.setup()

from api.models import (Especialidad, SalaAtencion, Medico, Paciente, 
                       ConsultaMedica, Tratamiento, Medicamento, RecetaMedica)

def cargar_datos():
    print("=== CARGANDO DATOS DE PRUEBA PARA SALUD VITAL ===")
    
    # Limpiar datos existentes (opcional - comentar si quieres mantener datos)
    print("Limpiando datos existentes...")
    RecetaMedica.objects.all().delete()
    Tratamiento.objects.all().delete()
    ConsultaMedica.objects.all().delete()
    Medicamento.objects.all().delete()
    Medico.objects.all().delete()
    Paciente.objects.all().delete()
    SalaAtencion.objects.all().delete()
    Especialidad.objects.all().delete()
    
    print("Creando especialidades...")
    # 1. ESPECIALIDADES
    especialidades_data = [
        {'nombre': 'Cardiología', 'descripcion': 'Especialidad en enfermedades del corazón'},
        {'nombre': 'Pediatría', 'descripcion': 'Especialidad en atención infantil'},
        {'nombre': 'Dermatología', 'descripcion': 'Especialidad en enfermedades de la piel'},
        {'nombre': 'Ginecología', 'descripcion': 'Especialidad en salud femenina'},
        {'nombre': 'Traumatología', 'descripcion': 'Especialidad en huesos y articulaciones'},
        {'nombre': 'Medicina General', 'descripcion': 'Atención primaria y general'},
    ]
    
    especialidades = []
    for esp in especialidades_data:
        especialidad = Especialidad.objects.create(**esp)
        especialidades.append(especialidad)
        print(f'  ✓ {especialidad.nombre}')
    
    print("Creando salas de atención...")
    # 2. SALAS DE ATENCIÓN
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
        print(f'  ✓ {sala_obj}')
    
    print("Creando médicos...")
    # 3. MÉDICOS
    medicos_data = [
        {'rut': '12.345.678-9', 'nombre': 'Carlos', 'apellido': 'López', 'especialidad': especialidades[0]},
        {'rut': '23.456.789-0', 'nombre': 'Ana', 'apellido': 'Martínez', 'especialidad': especialidades[1]},
        {'rut': '34.567.890-1', 'nombre': 'Roberto', 'apellido': 'García', 'especialidad': especialidades[2]},
        {'rut': '45.678.901-2', 'nombre': 'María', 'apellido': 'Rodríguez', 'especialidad': especialidades[3]},
        {'rut': '56.789.012-3', 'nombre': 'Pedro', 'apellido': 'Fernández', 'especialidad': especialidades[4]},
        {'rut': '67.890.123-4', 'nombre': 'Laura', 'apellido': 'Silva', 'especialidad': especialidades[5]},
    ]
    
    medicos = []
    for i, med in enumerate(medicos_data):
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
        print(f'  ✓ Dr. {medico.nombre} {medico.apellido} - {medico.especialidad.nombre}')
    
    print("Creando pacientes...")
    # 4. PACIENTES
    pacientes_data = [
        {'rut': '98.765.432-1', 'nombre': 'Juan', 'apellido': 'Pérez', 'fecha_nacimiento': '1985-03-15', 'genero': 'Masculino', 'tipo_sangre': 'A+'},
        {'rut': '87.654.321-2', 'nombre': 'Laura', 'apellido': 'González', 'fecha_nacimiento': '1990-07-22', 'genero': 'Femenino', 'tipo_sangre': 'O+'},
        {'rut': '76.543.210-3', 'nombre': 'Diego', 'apellido': 'Silva', 'fecha_nacimiento': '1978-11-30', 'genero': 'Masculino', 'tipo_sangre': 'B+'},
        {'rut': '65.432.109-4', 'nombre': 'Camila', 'apellido': 'Rojas', 'fecha_nacimiento': '1995-05-10', 'genero': 'Femenino', 'tipo_sangre': 'AB+'},
        {'rut': '54.321.098-5', 'nombre': 'Andrés', 'apellido': 'Mendoza', 'fecha_nacimiento': '1982-12-05', 'genero': 'Masculino', 'tipo_sangre': 'A-'},
        {'rut': '43.210.987-6', 'nombre': 'Valentina', 'apellido': 'Castro', 'fecha_nacimiento': '1988-09-18', 'genero': 'Femenino', 'tipo_sangre': 'O-'},
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
            direccion=f"Av. Principal #{random.randint(100, 999)}, Santiago",
            activo=True
        )
        pacientes.append(paciente)
        print(f'  ✓ {paciente.nombre} {paciente.apellido} - {paciente.genero} - {paciente.tipo_sangre}')
    
    print("Creando medicamentos...")
    # 5. MEDICAMENTOS
    medicamentos_data = [
        {'nombre': 'Paracetamol 500mg', 'laboratorio': 'Bayer', 'stock': 100, 'precio_unitario': 1500, 'tipo': 'Tableta'},
        {'nombre': 'Ibuprofeno 400mg', 'laboratorio': 'Pfizer', 'stock': 80, 'precio_unitario': 1200, 'tipo': 'Tableta'},
        {'nombre': 'Amoxicilina 500mg', 'laboratorio': 'Roche', 'stock': 50, 'precio_unitario': 3500, 'tipo': 'Tableta'},
        {'nombre': 'Jarabe para la tos', 'laboratorio': 'Johnson & Johnson', 'stock': 30, 'precio_unitario': 4500, 'tipo': 'Jarabe'},
        {'nombre': 'Insulina Glargina', 'laboratorio': 'Novo Nordisk', 'stock': 20, 'precio_unitario': 12000, 'tipo': 'Inyección'},
        {'nombre': 'Omeprazol 20mg', 'laboratorio': 'AstraZeneca', 'stock': 60, 'precio_unitario': 2800, 'tipo': 'Tableta'},
    ]
    
    medicamentos = []
    for med in medicamentos_data:
        medicamento = Medicamento.objects.create(**med)
        medicamentos.append(medicamento)
        print(f'  ✓ {medicamento.nombre} - Stock: {medicamento.stock}')
    
    print("Creando consultas médicas...")
    # 6. CONSULTAS MÉDICAS
    motivos = [
        "Control rutinario de salud",
        "Dolor de cabeza persistente",
        "Fiebre y malestar general", 
        "Dolor abdominal",
        "Control de presión arterial",
        "Seguimiento de tratamiento",
        "Consulta por alergias",
        "Examen médico laboral"
    ]
    
    diagnosticos = [
        "Gripe común - Reposo e hidratación",
        "Hipertensión arterial - Control periódico",
        "Gastritis - Dieta blanda y medicación",
        "Infección respiratoria superior - Antibióticos",
        "Diabetes tipo 2 - Control glucémico",
        "Ansiedad generalizada - Terapia y seguimiento",
        "Artritis reumatoide - Tratamiento especializado",
        "Salud óptima - Sin hallazgos relevantes"
    ]
    
    consultas = []
    for i in range(15):  # Crear 15 consultas
        consulta = ConsultaMedica.objects.create(
            paciente=random.choice(pacientes),
            medico=random.choice(medicos),
            sala=random.choice(salas),
            fecha_consulta=datetime.now() - timedelta(days=random.randint(1, 90)),
            motivo=random.choice(motivos),
            diagnostico=random.choice(diagnosticos),
            estado=random.choice(['Programada', 'Realizada', 'Realizada', 'Realizada'])  # Más realizadas
        )
        consultas.append(consulta)
        print(f'  ✓ Consulta: {consulta.paciente} con Dr. {consulta.medico} - {consulta.estado}')
    
    print("Creando tratamientos...")
    # 7. TRATAMIENTOS
    tratamientos = []
    for consulta in consultas:
        if consulta.estado == 'Realizada':
            tratamiento = Tratamiento.objects.create(
                consulta=consulta,
                descripcion=f"Tratamiento para {consulta.diagnostico.split(' - ')[0]}",
                duracion_dias=random.randint(7, 30),
                observaciones="Seguir indicaciones médicas y asistir a controles"
            )
            tratamientos.append(tratamiento)
            print(f'  ✓ Tratamiento: {tratamiento.descripcion} ({tratamiento.duracion_dias} días)')
    
    print("Creando recetas médicas...")
    # 8. RECETAS MÉDICAS
    dosis_options = ['1 tableta', '2 tabletas', '5 ml', '10 ml', '1 aplicación']
    frecuencia_options = ['Cada 8 horas', 'Cada 12 horas', 'Una vez al día', 'Cada 6 horas', 'Cada 24 horas']
    
    for tratamiento in tratamientos:
        # Crear 1-2 recetas por tratamiento
        for _ in range(random.randint(1, 2)):
            receta = RecetaMedica.objects.create(
                consulta=tratamiento.consulta,
                tratamiento=tratamiento,
                medicamento=random.choice(medicamentos),
                dosis=random.choice(dosis_options),
                frecuencia=random.choice(frecuencia_options),
                duracion=f"{random.randint(5, 15)} días",
                indicaciones="Tomar con alimentos. No suspender sin autorización médica."
            )
            print(f'  ✓ Receta: {receta.medicamento.nombre} - {receta.dosis} {receta.frecuencia}')
    
    print("\n" + "="*50)
    print("¡DATOS DE PRUEBA CARGADOS EXITOSAMENTE!")
    print("="*50)
    
    # Resumen final
    print(f"\nRESUMEN DE DATOS CARGADOS:")
    print(f"  • Especialidades: {Especialidad.objects.count()}")
    print(f"  • Salas: {SalaAtencion.objects.count()}")
    print(f"  • Médicos: {Medico.objects.count()}")
    print(f"  • Pacientes: {Paciente.objects.count()}")
    print(f"  • Medicamentos: {Medicamento.objects.count()}")
    print(f"  • Consultas: {ConsultaMedica.objects.count()}")
    print(f"  • Tratamientos: {Tratamiento.objects.count()}")
    print(f"  • Recetas: {RecetaMedica.objects.count()}")
    print(f"\nPuedes acceder al sistema en: http://localhost:8000/")

if __name__ == '__main__':
    cargar_datos()