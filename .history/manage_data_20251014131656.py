"""
Script para cargar datos de prueba en el sistema Salud Vital
"""
import os
import django
from datetime import date, timedelta, datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_vital.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Especialidad, Sala, Medico, Paciente, Consulta, Medicamento, Tratamiento, Receta, SeguimientoPaciente

def crear_datos_prueba():
    """Función principal para crear datos de prueba"""
    print("🚀 Creando datos de prueba para Salud Vital...")
    
    # Crear especialidades
    print("📚 Creando especialidades...")
    especialidades_data = [
        'Cardiología', 'Pediatría', 'Dermatología', 'Neurología', 
        'Ortopedia', 'Ginecología', 'Medicina General', 'Psiquiatría'
    ]
    
    especialidades = {}
    for esp in especialidades_data:
        obj, created = Especialidad.objects.get_or_create(nombre=esp)
        especialidades[esp] = obj
        if created:
            print(f"  ✅ {esp}")
    
    # Crear salas
    print("\n🏢 Creando salas...")
    salas_data = [
        {'nombre': 'Consulta General 1', 'numero': '101', 'piso': 1, 'capacidad': 5},
        {'nombre': 'Consulta General 2', 'numero': '102', 'piso': 1, 'capacidad': 5},
        {'nombre': 'Cardiología', 'numero': '201', 'piso': 2, 'capacidad': 3},
        {'nombre': 'Pediatría', 'numero': '202', 'piso': 2, 'capacidad': 4},
        {'nombre': 'Urgencia', 'numero': '001', 'piso': 1, 'capacidad': 2},
    ]
    
    salas = {}
    for sala in salas_data:
        obj, created = Sala.objects.get_or_create(
            numero=sala['numero'],
            defaults=sala
        )
        salas[sala['numero']] = obj
        if created:
            print(f"  ✅ Sala {sala['numero']} - {sala['nombre']}")
    
    # Crear usuarios médicos
    print("\n👨‍⚕️ Creando médicos...")
    medicos_data = [
        {'username': 'cardio1', 'first_name': 'Carlos', 'last_name': 'López', 'email': 'cardio@clinica.cl', 'especialidad': 'Cardiología'},
        {'username': 'pediatra1', 'first_name': 'Ana', 'last_name': 'Martínez', 'email': 'pediatra@clinica.cl', 'especialidad': 'Pediatría'},
        {'username': 'derma1', 'first_name': 'Laura', 'last_name': 'Gómez', 'email': 'derma@clinica.cl', 'especialidad': 'Dermatología'},
        {'username': 'general1', 'first_name': 'Roberto', 'last_name': 'Silva', 'email': 'general@clinica.cl', 'especialidad': 'Medicina General'},
    ]
    
    medicos = {}
    for med in medicos_data:
        user, created = User.objects.get_or_create(
            username=med['username'],
            defaults={
                'first_name': med['first_name'],
                'last_name': med['last_name'],
                'email': med['email'],
                'password': 'backend123'
            }
        )
        
        medico_obj, med_created = Medico.objects.get_or_create(
            user=user,
            defaults={
                'especialidad': especialidades[med['especialidad']],
                'telefono': '+56 9 1234 5678',
                'direccion': 'Av. Principal 123, Santiago'
            }
        )
        medicos[med['username']] = medico_obj
        if med_created:
            print(f"  ✅ Dr. {med['first_name']} {med['last_name']} - {med['especialidad']}")
    
    # Crear pacientes
    print("\n👥 Creando pacientes...")
    pacientes_data = [
        {'rut': '12.345.678-9', 'nombre': 'Juan', 'apellido': 'Pérez', 'fecha_nacimiento': date(1985, 5, 15), 'genero': 'M', 'tipo_sangre': 'A+'},
        {'rut': '23.456.789-0', 'nombre': 'María', 'apellido': 'González', 'fecha_nacimiento': date(1990, 8, 22), 'genero': 'F', 'tipo_sangre': 'O+'},
        {'rut': '34.567.890-1', 'nombre': 'Pedro', 'apellido': 'Rodríguez', 'fecha_nacimiento': date(1978, 3, 10), 'genero': 'M', 'tipo_sangre': 'B-'},
        {'rut': '45.678.901-2', 'nombre': 'Ana', 'apellido': 'López', 'fecha_nacimiento': date(2000, 12, 5), 'genero': 'F', 'tipo_sangre': 'AB+'},
    ]
    
    pacientes = {}
    for pac in pacientes_data:
        obj, created = Paciente.objects.get_or_create(
            rut=pac['rut'],
            defaults=pac
        )
        pacientes[pac['rut']] = obj
        if created:
            print(f"  ✅ {pac['nombre']} {pac['apellido']} - {pac['rut']}")
    
    # Crear medicamentos
    print("\n💊 Creando medicamentos...")
    medicamentos_data = [
        {'nombre': 'Paracetamol 500mg', 'laboratorio': 'LabChile', 'precio_unitario': 1500, 'stock': 100, 'tipo': 'Tableta'},
        {'nombre': 'Ibuprofeno 400mg', 'laboratorio': 'PharmaCorp', 'precio_unitario': 1800, 'stock': 80, 'tipo': 'Tableta'},
        {'nombre': 'Amoxicilina 250mg', 'laboratorio': 'BioLab', 'precio_unitario': 2500, 'stock': 50, 'tipo': 'Cápsula'},
        {'nombre': 'Jarabe para la tos', 'laboratorio': 'NaturalHealth', 'precio_unitario': 3200, 'stock': 30, 'tipo': 'Jarabe'},
    ]
    
    medicamentos = {}
    for med in medicamentos_data:
        obj, created = Medicamento.objects.get_or_create(
            nombre=med['nombre'],
            defaults=med
        )
        medicamentos[med['nombre']] = obj
        if created:
            print(f"  ✅ {med['nombre']} - Stock: {med['stock']}")
    
    print("\n🎉 ¡Datos de prueba creados exitosamente!")
    print("\n📊 Resumen:")
    print(f"   • Especialidades: {Especialidad.objects.count()}")
    print(f"   • Salas: {Sala.objects.count()}")
    print(f"   • Médicos: {Medico.objects.count()}")
    print(f"   • Pacientes: {Paciente.objects.count()}")
    print(f"   • Medicamentos: {Medicamento.objects.count()}")

if __name__ == '__main__':
    crear_datos_prueba()