"""
Vistas CRUD para el sistema Salud Vital
Vistas basadas en funciones para los templates
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from .models import Paciente, Medico, Medicamento, Consulta, Receta, Tratamiento, Sala, Especialidad, SeguimientoPaciente

# ========== VISTAS CRUD PRINCIPALES ==========

def crud_pacientes(request):
    """Vista para listar pacientes"""
    pacientes = Paciente.objects.all()
    
    # Filtros
    query = request.GET.get('q', '')
    genero = request.GET.get('genero', '')
    tipo_sangre = request.GET.get('tipo_sangre', '')
    activo = request.GET.get('activo', '')
    
    if query:
        pacientes = pacientes.filter(
            models.Q(nombre__icontains=query) | 
            models.Q(apellido__icontains=query) |
            models.Q(rut__icontains=query)
        )
    
    if genero:
        pacientes = pacientes.filter(genero=genero)
    
    if tipo_sangre:
        pacientes = pacientes.filter(tipo_sangre=tipo_sangre)
    
    if activo:
        pacientes = pacientes.filter(activo=activo == 'true')
    
    return render(request, 'crud_pacientes.html', {'pacientes': pacientes})

def crud_medicos(request):
    """Vista para listar médicos"""
    medicos = Medico.objects.all()
    especialidades = Especialidad.objects.all()
    
    # Filtros
    query = request.GET.get('q', '')
    especialidad_id = request.GET.get('especialidad', '')
    
    if query:
        medicos = medicos.filter(
            models.Q(user__first_name__icontains=query) | 
            models.Q(user__last_name__icontains=query) |
            models.Q(user__username__icontains=query)
        )
    
    if especialidad_id:
        medicos = medicos.filter(especialidad_id=especialidad_id)
    
    return render(request, 'crud_medicos.html', {
        'medicos': medicos,
        'especialidades': especialidades
    })

def crud_medicamentos(request):
    """Vista para listar medicamentos"""
    medicamentos = Medicamento.objects.all()
    return render(request, 'crud_medicamentos.html', {'medicamentos': medicamentos})

def crud_especialidades(request):
    """Vista para listar especialidades"""
    especialidades = Especialidad.objects.all()
    return render(request, 'crud_especialidades.html', {'especialidades': especialidades})

def crud_salas(request):
    """Vista para listar salas - CORREGIDA"""
    # Cargar solo los campos básicos para evitar errores
    salas = Sala.objects.only('id', 'nombre', 'numero', 'piso', 'capacidad').all()
    
    return render(request, 'crud_salas.html', {'salas': salas})

def crud_seguimientos(request):
    """Vista para listar seguimientos de pacientes"""
    seguimientos = SeguimientoPaciente.objects.all()
    return render(request, 'crud_seguimientos.html', {'seguimientos': seguimientos})

def crud_consultas(request):
    """Vista para listar consultas - CORREGIDA"""
    # Cargar consultas sin los campos problemáticos de Sala
    consultas = Consulta.objects.select_related('paciente', 'medico').all()
    
    return render(request, 'crud_consultas.html', {'consultas': consultas})

# ========== CREAR ==========

def crear_paciente(request):
    """Vista para crear paciente - CORREGIDA"""
    if request.method == 'POST':
        try:
            Paciente.objects.create(
                rut=request.POST['rut'],
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                fecha_nacimiento=request.POST['fecha_nacimiento'],
                genero=request.POST['genero'],  # Ahora acepta valores completos
                tipo_sangre=request.POST['tipo_sangre'],
                telefono=request.POST.get('telefono', ''),
                correo=request.POST.get('correo', ''),
                direccion=request.POST.get('direccion', ''),
                activo=True
            )
            messages.success(request, '✅ Paciente creado exitosamente!')
            return redirect('crud:crud_pacientes')
        except Exception as e:
            messages.error(request, f'❌ Error al crear paciente: {str(e)}')
    
    return render(request, 'crear_paciente.html')

def crear_medico(request):
    """Vista para crear médico"""
    especialidades = Especialidad.objects.all()
    
    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        especialidad_id = request.POST.get('especialidad')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        
        try:
            # Validar campos requeridos
            if not all([rut, nombre, apellido, especialidad_id]):
                messages.error(request, '❌ Todos los campos marcados con * son obligatorios.')
                return render(request, 'crear_medico.html', {
                    'especialidades': especialidades
                })
            
            # Verificar si la especialidad existe
            especialidad = Especialidad.objects.get(id=especialidad_id)
            
            # Crear usuario de Django primero
            username = rut.replace('.', '').replace('-', '').lower()
            
            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                messages.error(request, '❌ Ya existe un médico con este RUT.')
                return render(request, 'crear_medico.html', {
                    'especialidades': especialidades
                })
            
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                password='temp123',  # Contraseña temporal
                first_name=nombre,
                last_name=apellido,
                email=correo
            )
            
            # Crear el médico vinculado al usuario
            medico = Medico.objects.create(
                user=user,
                especialidad=especialidad,
                telefono=telefono
            )
            
            messages.success(request, f'✅ Médico {nombre} {apellido} creado exitosamente!')
            return redirect('crud:crud_medicos')
            
        except Especialidad.DoesNotExist:
            messages.error(request, '❌ La especialidad seleccionada no existe.')
        except Exception as e:
            messages.error(request, f'❌ Error al crear el médico: {str(e)}')
    
    # Si es GET o hay errores
    return render(request, 'crear_medico.html', {
        'especialidades': especialidades
    })

def crear_medicamento(request):
    """Vista para crear medicamento"""
    if request.method == 'POST':
        try:
            Medicamento.objects.create(
                nombre=request.POST['nombre'],
                laboratorio=request.POST.get('laboratorio', ''),
                precio_unitario=request.POST.get('precio_unitario', 0),
                stock=request.POST.get('stock', 0),
                tipo=request.POST.get('tipo', 'Tableta')
            )
            messages.success(request, '✅ Medicamento creado exitosamente!')
            return redirect('crud:crud_medicamentos')
        except Exception as e:
            messages.error(request, f'❌ Error al crear medicamento: {str(e)}')
    
    return render(request, 'crear_medicamento.html')

def crear_especialidad(request):
    """Vista para crear especialidad - CORREGIDA"""
    if request.method == 'POST':
        try:
            # CORREGIDO: Ahora incluye la descripción
            Especialidad.objects.create(
                nombre=request.POST['nombre'],
                descripcion=request.POST.get('descripcion', '')  # ← ESTA LÍNEA FALTABA
            )
            messages.success(request, '✅ Especialidad creada exitosamente!')
            return redirect('crud:crud_especialidades')
        except Exception as e:
            messages.error(request, f'❌ Error al crear especialidad: {str(e)}')
    
    return render(request, 'crear_especialidad.html')

def crear_sala(request):
    """Vista para crear sala"""
    especialidades = Especialidad.objects.all()
    
    if request.method == 'POST':
        try:
            sala = Sala.objects.create(
                nombre=request.POST['nombre'],
                numero=request.POST['numero'],
                piso=request.POST.get('piso', 1),
                capacidad=request.POST.get('capacidad', 5),
                tipo=request.POST.get('tipo', 'Consulta'),
                especialidad_id=request.POST.get('especialidad') or None,
                equipamiento=request.POST.get('equipamiento', ''),
                disponible=request.POST.get('disponible') == 'on',
                estado=request.POST.get('estado', 'Disponible'),
                descripcion=request.POST.get('descripcion', '')
            )
            
            messages.success(request, '✅ Sala creada exitosamente!')
            return redirect('crud:crud_salas')
        except Exception as e:
            messages.error(request, f'❌ Error al crear sala: {str(e)}')
    
    return render(request, 'crear_sala.html', {
        'especialidades': especialidades
    })

def crear_consulta(request):
    """Vista para crear consulta - CORREGIDA"""
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    
    # Cargar solo los campos básicos de Sala para evitar errores
    salas = Sala.objects.only('id', 'nombre', 'piso', 'numero', 'capacidad').all()
    
    if request.method == 'POST':
        try:
            paciente_id = request.POST.get('paciente')
            medico_id = request.POST.get('medico')
            sala_id = request.POST.get('sala')
            fecha = request.POST.get('fecha')
            motivo = request.POST.get('motivo')
            diagnostico = request.POST.get('diagnostico')
            estado = request.POST.get('estado')
            
            consulta = Consulta(
                paciente_id=paciente_id,
                medico_id=medico_id,
                sala_id=sala_id if sala_id else None,
                fecha=fecha,
                motivo=motivo,
                diagnostico=diagnostico,
                estado=estado
            )
            consulta.save()
            
            messages.success(request, '✅ Consulta creada exitosamente!')
            return redirect('crud:crud_consultas')
            
        except Exception as e:
            messages.error(request, f'❌ Error al crear consulta: {str(e)}')
    
    return render(request, 'crear_consulta.html', {
        'pacientes': pacientes,
        'medicos': medicos,
        'salas': salas
    })

def crear_seguimiento(request):
    """Vista para crear seguimiento"""
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    
    if request.method == 'POST':
        try:
            SeguimientoPaciente.objects.create(
                paciente_id=request.POST['paciente'],
                medico_id=request.POST['medico'],
                fecha_seguimiento=request.POST['fecha_seguimiento'],
                observaciones=request.POST['observaciones'],
                proxima_cita=request.POST.get('proxima_cita'),
                peso=request.POST.get('peso'),
                altura=request.POST.get('altura'),
                presion_arterial=request.POST.get('presion_arterial'),
                temperatura=request.POST.get('temperatura')
            )
            messages.success(request, '✅ Seguimiento creado exitosamente!')
            return redirect('crud:crud_seguimientos')
        except Exception as e:
            messages.error(request, f'❌ Error al crear seguimiento: {str(e)}')
    
    return render(request, 'crear_seguimiento.html', {
        'pacientes': pacientes,
        'medicos': medicos
    })

# ========== EDITAR ==========

def editar_paciente(request, id):
    """Vista para editar paciente - CORREGIDA"""
    paciente = get_object_or_404(Paciente, id=id)
    
    if request.method == 'POST':
        try:
            paciente.rut = request.POST['rut']
            paciente.nombre = request.POST['nombre']
            paciente.apellido = request.POST['apellido']
            paciente.fecha_nacimiento = request.POST['fecha_nacimiento']
            paciente.genero = request.POST['genero']  # Ahora acepta valores completos
            paciente.tipo_sangre = request.POST['tipo_sangre']
            paciente.telefono = request.POST.get('telefono', '')
            paciente.correo = request.POST.get('correo', '')
            paciente.direccion = request.POST.get('direccion', '')
            paciente.activo = request.POST.get('activo') == 'on'
            paciente.save()
            
            messages.success(request, '✅ Paciente actualizado exitosamente!')
            return redirect('crud:crud_pacientes')
        except Exception as e:
            messages.error(request, f'❌ Error al actualizar paciente: {str(e)}')
    
    return render(request, 'editar_paciente.html', {'paciente': paciente})

def editar_medico(request, id):
    """Vista para editar médico"""
    medico = get_object_or_404(Medico, id=id)
    especialidades = Especialidad.objects.all()
    
    if request.method == 'POST':
        try:
            # Actualizar datos del usuario
            medico.user.first_name = request.POST['nombre']
            medico.user.last_name = request.POST['apellido']
            medico.user.email = request.POST.get('correo', '')
            medico.user.save()
            
            # Actualizar datos del médico
            medico.especialidad_id = request.POST['especialidad']
            medico.telefono = request.POST.get('telefono', '')
            medico.save()
            
            messages.success(request, '✅ Médico actualizado exitosamente!')
            return redirect('crud:crud_medicos')
        except Exception as e:
            messages.error(request, f'❌ Error al actualizar médico: {str(e)}')
    
    return render(request, 'editar_medico.html', {
        'medico': medico,
        'especialidades': especialidades
    })

def editar_medicamento(request, id):
    """Vista para editar medicamento"""
    medicamento = get_object_or_404(Medicamento, id=id)
    
    if request.method == 'POST':
        try:
            medicamento.nombre = request.POST['nombre']
            medicamento.laboratorio = request.POST.get('laboratorio', '')
            medicamento.precio_unitario = request.POST.get('precio_unitario', 0)
            medicamento.stock = request.POST.get('stock', 0)
            medicamento.tipo = request.POST.get('tipo', 'Tableta')
            medicamento.save()
            
            messages.success(request, '✅ Medicamento actualizado exitosamente!')
            return redirect('crud:crud_medicamentos')
        except Exception as e:
            messages.error(request, f'❌ Error al actualizar medicamento: {str(e)}')
    
    return render(request, 'editar_medicamento.html', {'medicamento': medicamento})

def editar_especialidad(request, id):
    """Vista para editar especialidad"""
    especialidad = get_object_or_404(Especialidad, id=id)
    
    if request.method == 'POST':
        try:
            # CORREGIDO: Solo actualizar nombre, sin descripcion
            especialidad.nombre = request.POST['nombre']
            especialidad.save()
            
            messages.success(request, '✅ Especialidad actualizada exitosamente!')
            return redirect('crud:crud_especialidades')
        except Exception as e:
            messages.error(request, f'❌ Error al actualizar especialidad: {str(e)}')
    
    return render(request, 'editar_especialidad.html', {'especialidad': especialidad})

def editar_sala(request, id):
    """Vista para editar sala"""
    sala = get_object_or_404(Sala, id=id)
    especialidades = Especialidad.objects.all()
    
    if request.method == 'POST':
        try:
            sala.nombre = request.POST['nombre']
            sala.numero = request.POST['numero']
            sala.piso = request.POST.get('piso', 1)
            sala.capacidad = request.POST.get('capacidad', 5)
            sala.tipo = request.POST.get('tipo', 'Consulta')
            
            # AGREGAR ESPECIALIDAD:
            especialidad_id = request.POST.get('especialidad')
            if especialidad_id:
                sala.especialidad_id = especialidad_id
            else:
                sala.especialidad = None
            
            # AGREGAR LOS NUEVOS CAMPOS:
            sala.equipamiento = request.POST.get('equipamiento', '')
            sala.disponible = request.POST.get('disponible') == 'on'
            sala.estado = request.POST.get('estado', 'Disponible')
            sala.descripcion = request.POST.get('descripcion', '')
            
            sala.save()
            
            messages.success(request, '✅ Sala actualizada exitosamente!')
            return redirect('crud:crud_salas')
        except Exception as e:
            messages.error(request, f'❌ Error al actualizar sala: {str(e)}')
    
    return render(request, 'editar_sala.html', {
        'sala': sala,
        'especialidades': especialidades
    })

def editar_consulta(request, id):
    """Vista para editar consulta - CORREGIDA"""
    consulta = get_object_or_404(Consulta, id=id)
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    
    # Cargar solo los campos básicos de Sala para evitar errores
    salas = Sala.objects.only('id', 'nombre', 'piso', 'numero', 'capacidad').all()
    
    if request.method == 'POST':
        try:
            consulta.paciente_id = request.POST['paciente']
            consulta.medico_id = request.POST['medico']
            consulta.sala_id = request.POST.get('sala')
            consulta.fecha = request.POST['fecha']
            consulta.motivo = request.POST['motivo']
            consulta.diagnostico = request.POST.get('diagnostico', '')
            consulta.estado = request.POST.get('estado', 'programada')
            consulta.save()
            
            messages.success(request, '✅ Consulta actualizada exitosamente!')
            return redirect('crud:crud_consultas')
        except Exception as e:
            messages.error(request, f'❌ Error al actualizar consulta: {str(e)}')
    
    return render(request, 'editar_consulta.html', {
        'consulta': consulta,
        'pacientes': pacientes,
        'medicos': medicos,
        'salas': salas
    })

def editar_seguimiento(request, id):
    """Vista para editar seguimiento"""
    seguimiento = get_object_or_404(SeguimientoPaciente, id=id)
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    
    if request.method == 'POST':
        try:
            seguimiento.paciente_id = request.POST['paciente']
            seguimiento.medico_id = request.POST['medico']
            seguimiento.fecha_seguimiento = request.POST['fecha_seguimiento']
            seguimiento.observaciones = request.POST['observaciones']
            seguimiento.proxima_cita = request.POST.get('proxima_cita')
            seguimiento.peso = request.POST.get('peso')
            seguimiento.altura = request.POST.get('altura')
            seguimiento.presion_arterial = request.POST.get('presion_arterial')
            seguimiento.temperatura = request.POST.get('temperatura')
            seguimiento.save()
            
            messages.success(request, '✅ Seguimiento actualizado exitosamente!')
            return redirect('crud:crud_seguimientos')
        except Exception as e:
            messages.error(request, f'❌ Error al actualizar seguimiento: {str(e)}')
    
    return render(request, 'editar_seguimiento.html', {
        'seguimiento': seguimiento,
        'pacientes': pacientes,
        'medicos': medicos
    })

# ========== ELIMINAR ==========

def eliminar_paciente(request, id):
    """Vista para eliminar paciente"""
    paciente = get_object_or_404(Paciente, id=id)
    
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, '✅ Paciente eliminado exitosamente!')
        return redirect('crud:crud_pacientes')
    
    return render(request, 'eliminar_paciente.html', {'paciente': paciente})

def eliminar_medico(request, id):
    """Vista para eliminar médico"""
    medico = get_object_or_404(Medico, id=id)
    
    if request.method == 'POST':
        # Eliminar también el usuario asociado
        user = medico.user
        medico.delete()
        user.delete()
        
        messages.success(request, '✅ Médico eliminado exitosamente!')
        return redirect('crud:crud_medicos')
    
    return render(request, 'eliminar_medico.html', {'medico': medico})

def eliminar_medicamento(request, id):
    """Vista para eliminar medicamento"""
    medicamento = get_object_or_404(Medicamento, id=id)
    
    if request.method == 'POST':
        medicamento.delete()
        messages.success(request, '✅ Medicamento eliminado exitosamente!')
        return redirect('crud:crud_medicamentos')
    
    return render(request, 'eliminar_medicamento.html', {'medicamento': medicamento})

def eliminar_especialidad(request, id):
    """Vista para eliminar especialidad"""
    especialidad = get_object_or_404(Especialidad, id=id)
    
    if request.method == 'POST':
        especialidad.delete()
        messages.success(request, '✅ Especialidad eliminada exitosamente!')
        return redirect('crud:crud_especialidades')
    
    return render(request, 'eliminar_especialidad.html', {'especialidad': especialidad})

def eliminar_sala(request, id):
    """Vista para eliminar sala"""
    sala = get_object_or_404(Sala, id=id)
    
    if request.method == 'POST':
        sala.delete()
        messages.success(request, '✅ Sala eliminada exitosamente!')
        return redirect('crud:crud_salas')
    
    return render(request, 'eliminar_sala.html', {'sala': sala})

def eliminar_consulta(request, id):
    """Vista para eliminar consulta"""
    consulta = get_object_or_404(Consulta, id=id)
    
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, '✅ Consulta eliminada exitosamente!')
        return redirect('crud:crud_consultas')
    
    return render(request, 'eliminar_consulta.html', {'consulta': consulta})

def eliminar_seguimiento(request, id):
    """Vista para eliminar seguimiento"""
    seguimiento = get_object_or_404(SeguimientoPaciente, id=id)
    
    if request.method == 'POST':
        seguimiento.delete()
        messages.success(request, '✅ Seguimiento eliminado exitosamente!')
        return redirect('crud:crud_seguimientos')
    
    return render(request, 'eliminar_seguimiento.html', {'seguimiento': seguimiento})

# Vistas para Recetas
def crud_recetas(request):
    recetas = Receta.objects.all().select_related('consulta__paciente', 'consulta__medico', 'medicamento')
    return render(request, 'crud_recetas.html', {'recetas': recetas})

def crear_receta(request):
    consultas = Consulta.objects.all().select_related('paciente', 'medico')
    medicamentos = Medicamento.objects.all()
    
    if request.method == 'POST':
        try:
            consulta_id = request.POST.get('consulta')
            medicamento_id = request.POST.get('medicamento')
            dosis = request.POST.get('dosis')
            frecuencia = request.POST.get('frecuencia')
            duracion = request.POST.get('duracion')
            instrucciones = request.POST.get('instrucciones')
            
            receta = Receta(
                consulta_id=consulta_id,
                medicamento_id=medicamento_id,
                dosis=dosis,
                frecuencia=frecuencia,
                duracion=duracion,
                instrucciones=instrucciones
            )
            receta.save()
            
            messages.success(request, '✅ Receta creada exitosamente!')
            return redirect('crud:crud_recetas')
            
        except Exception as e:
            messages.error(request, f'❌ Error al crear receta: {str(e)}')
    
    return render(request, 'crear_receta.html', {
        'consultas': consultas,
        'medicamentos': medicamentos
    })

def editar_receta(request, id):
    try:
        receta = Receta.objects.get(id=id)
        consultas = Consulta.objects.all().select_related('paciente', 'medico')
        medicamentos = Medicamento.objects.all()
        
        if request.method == 'POST':
            receta.consulta_id = request.POST.get('consulta')
            receta.medicamento_id = request.POST.get('medicamento')
            receta.dosis = request.POST.get('dosis')
            receta.frecuencia = request.POST.get('frecuencia')
            receta.duracion = request.POST.get('duracion')
            receta.instrucciones = request.POST.get('instrucciones')
            receta.save()
            
            messages.success(request, '✅ Receta actualizada exitosamente!')
            return redirect('crud:crud_recetas')
            
        return render(request, 'editar_receta.html', {
            'receta': receta,
            'consultas': consultas,
            'medicamentos': medicamentos
        })
        
    except Receta.DoesNotExist:
        messages.error(request, '❌ La receta no existe.')
        return redirect('crud:crud_recetas')

def eliminar_receta(request, id):
    try:
        receta = Receta.objects.get(id=id)
        if request.method == 'POST':
            receta.delete()
            messages.success(request, '✅ Receta eliminada exitosamente!')
            return redirect('crud:crud_recetas')
            
        return render(request, 'eliminar_receta.html', {'receta': receta})
        
    except Receta.DoesNotExist:
        messages.error(request, '❌ La receta no existe.')
        return redirect('crud:crud_recetas')

# Vistas para Tratamientos
def crud_tratamientos(request):
    tratamientos = Tratamiento.objects.all().select_related('consulta__paciente', 'consulta__medico')
    return render(request, 'crud_tratamientos.html', {'tratamientos': tratamientos})

def crear_tratamiento(request):
    """Vista para crear tratamiento - COMPLETA Y DEFINITIVA"""
    consultas = Consulta.objects.all().select_related('paciente', 'medico')
    medicamentos = Medicamento.objects.all()
    
    if request.method == 'POST':
        try:
            consulta_id = request.POST.get('consulta')
            medicamento_nombre = request.POST.get('medicamento')
            dosis = request.POST.get('dosis')
            duracion = request.POST.get('duracion')
            instrucciones = request.POST.get('instrucciones')
            
            # Validar campos requeridos
            if not all([consulta_id, medicamento_nombre, dosis, duracion]):
                messages.error(request, '❌ Todos los campos marcados con * son obligatorios.')
                return render(request, 'crear_tratamiento.html', {
                    'consultas': consultas,
                    'medicamentos': medicamentos
                })
            
            # Crear el tratamiento
            tratamiento = Tratamiento(
                consulta_id=consulta_id,
                medicamento=medicamento_nombre,
                dosis=dosis,
                duracion=duracion,
                instrucciones=instrucciones
            )
            tratamiento.save()
            
            messages.success(request, '✅ Tratamiento creado exitosamente!')
            return redirect('crud:crud_tratamientos')
            
        except Exception as e:
            messages.error(request, f'❌ Error al crear tratamiento: {str(e)}')
    
    return render(request, 'crear_tratamiento.html', {
        'consultas': consultas,
        'medicamentos': medicamentos
    })

def editar_tratamiento(request, id):
    """Vista para editar tratamiento - COMPLETAMENTE CORREGIDA"""
    try:
        tratamiento = Tratamiento.objects.get(id=id)
        consultas = Consulta.objects.all().select_related('paciente', 'medico')
        medicamentos = Medicamento.objects.all()  # Obtener todos los medicamentos
        
        print(f"🔍 DEBUG: Tratamiento ID {tratamiento.id}")
        print(f"🔍 DEBUG: Medicamento actual: {tratamiento.medicamento}")
        print(f"🔍 DEBUG: Total de medicamentos en BD: {medicamentos.count()}")
        
        # DEBUG: Mostrar todos los medicamentos disponibles
        for i, med in enumerate(medicamentos):
            print(f"🔍 DEBUG: Medicamento {i+1}: {med.nombre} - {med.laboratorio}")
        
        if request.method == 'POST':
            try:
                # Obtener datos del formulario
                consulta_id = request.POST.get('consulta')
                medicamento_nombre = request.POST.get('medicamento')
                dosis = request.POST.get('dosis')
                duracion = request.POST.get('duracion')
                instrucciones = request.POST.get('instrucciones')
                
                print(f"🔍 DEBUG POST: medicamento seleccionado = {medicamento_nombre}")
                
                # Validar campos requeridos
                if not all([consulta_id, medicamento_nombre, dosis, duracion]):
                    messages.error(request, '❌ Todos los campos marcados con * son obligatorios.')
                    return render(request, 'editar_tratamiento.html', {
                        'tratamiento': tratamiento,
                        'consultas': consultas,
                        'medicamentos': medicamentos
                    })
                
                # Actualizar el tratamiento
                tratamiento.consulta_id = consulta_id
                tratamiento.medicamento = medicamento_nombre
                tratamiento.dosis = dosis
                tratamiento.duracion = duracion
                tratamiento.instrucciones = instrucciones
                tratamiento.save()
                
                messages.success(request, '✅ Tratamiento actualizado exitosamente!')
                return redirect('crud:crud_tratamientos')
                
            except Exception as e:
                messages.error(request, f'❌ Error al actualizar tratamiento: {str(e)}')
                print(f"❌ ERROR: {e}")
        
        # Pasar datos al template
        context = {
            'tratamiento': tratamiento,
            'consultas': consultas,
            'medicamentos': medicamentos  # ← ESTO ES LO MÁS IMPORTANTE
        }
        
        print(f"🔍 DEBUG: Enviando {len(medicamentos)} medicamentos al template")
        return render(request, 'editar_tratamiento.html', context)
        
    except Tratamiento.DoesNotExist:
        messages.error(request, '❌ El tratamiento no existe.')
        return redirect('crud:crud_tratamientos')
    except Exception as e:
        messages.error(request, f'❌ Error al cargar el tratamiento: {str(e)}')
        print(f"❌ ERROR GENERAL: {e}")
        return redirect('crud:crud_tratamientos')

def editar_tratamiento(request, id):
    """Vista para editar tratamiento - CORREGIDA DEFINITIVA"""
    try:
        # Obtener el tratamiento
        tratamiento = Tratamiento.objects.get(id=id)
        
        # OBTENER LOS MEDICAMENTOS - ESTA LÍNEA ES CLAVE
        medicamentos = Medicamento.objects.all()
        consultas = Consulta.objects.all().select_related('paciente', 'medico')
        
        if request.method == 'POST':
            try:
                # Obtener datos del formulario
                consulta_id = request.POST.get('consulta')
                medicamento_nombre = request.POST.get('medicamento')  # Nombre del medicamento seleccionado
                dosis = request.POST.get('dosis')
                duracion = request.POST.get('duracion')
                instrucciones = request.POST.get('instrucciones')
                
                # Validar campos requeridos
                if not all([consulta_id, medicamento_nombre, dosis, duracion]):
                    messages.error(request, '❌ Todos los campos marcados con * son obligatorios.')
                    return render(request, 'editar_tratamiento.html', {
                        'tratamiento': tratamiento,
                        'consultas': consultas,
                        'medicamentos': medicamentos  # Mantener medicamentos en caso de error
                    })
                
                # Actualizar el tratamiento
                tratamiento.consulta_id = consulta_id
                tratamiento.medicamento = medicamento_nombre  # Guardar el nombre del medicamento
                tratamiento.dosis = dosis
                tratamiento.duracion = duracion
                tratamiento.instrucciones = instrucciones
                tratamiento.save()
                
                messages.success(request, '✅ Tratamiento actualizado exitosamente!')
                return redirect('crud:crud_tratamientos')
                
            except Exception as e:
                messages.error(request, f'❌ Error al actualizar tratamiento: {str(e)}')
        
        # PASAR MEDICAMENTOS AL TEMPLATE - ESTO ES LO MÁS IMPORTANTE
        context = {
            'tratamiento': tratamiento,
            'consultas': consultas,
            'medicamentos': medicamentos  # ← ESTA LÍNEA FALTABA
        }
        
        return render(request, 'editar_tratamiento.html', context)
        
    except Tratamiento.DoesNotExist:
        messages.error(request, '❌ El tratamiento no existe.')
        return redirect('crud:crud_tratamientos')
    except Exception as e:
        messages.error(request, f'❌ Error al cargar el tratamiento: {str(e)}')
        return redirect('crud:crud_tratamientos')

def crear_tratamiento(request):
    """Vista para crear tratamiento - CORREGIDA"""
    consultas = Consulta.objects.all().select_related('paciente', 'medico')
    medicamentos = Medicamento.objects.all()  # ← OBTENER MEDICAMENTOS
    
    if request.method == 'POST':
        try:
            consulta_id = request.POST.get('consulta')
            medicamento_nombre = request.POST.get('medicamento')
            dosis = request.POST.get('dosis')
            duracion = request.POST.get('duracion')
            instrucciones = request.POST.get('instrucciones')
            
            # Validar campos requeridos
            if not all([consulta_id, medicamento_nombre, dosis, duracion]):
                messages.error(request, '❌ Todos los campos marcados con * son obligatorios.')
                return render(request, 'crear_tratamiento.html', {
                    'consultas': consultas,
                    'medicamentos': medicamentos  # ← MANTENER EN ERROR
                })
            
            # Crear el tratamiento
            tratamiento = Tratamiento(
                consulta_id=consulta_id,
                medicamento=medicamento_nombre,
                dosis=dosis,
                duracion=duracion,
                instrucciones=instrucciones
            )
            tratamiento.save()
            
            messages.success(request, '✅ Tratamiento creado exitosamente!')
            return redirect('crud:crud_tratamientos')
            
        except Exception as e:
            messages.error(request, f'❌ Error al crear tratamiento: {str(e)}')
    
    return render(request, 'crear_tratamiento.html', {
        'consultas': consultas,
        'medicamentos': medicamentos  # ← PASAR MEDICAMENTOS AL TEMPLATE
    })

def editar_tratamiento(request, id):
    try:
        tratamiento = Tratamiento.objects.get(id=id)
        consultas = Consulta.objects.all().select_related('paciente', 'medico')
        
        if request.method == 'POST':
            tratamiento.consulta_id = request.POST.get('consulta')
            tratamiento.medicamento = request.POST.get('medicamento')
            tratamiento.dosis = request.POST.get('dosis')
            tratamiento.duracion = request.POST.get('duracion')
            tratamiento.instrucciones = request.POST.get('instrucciones')
            tratamiento.save()
            
            messages.success(request, '✅ Tratamiento actualizada exitosamente!')
            return redirect('crud:crud_tratamientos')
            
        return render(request, 'editar_tratamiento.html', {
            'tratamiento': tratamiento,
            'consultas': consultas
        })
        
    except Tratamiento.DoesNotExist:
        messages.error(request, '❌ El tratamiento no existe.')
        return redirect('crud:crud_tratamientos')

def eliminar_tratamiento(request, id):
    try:
        tratamiento = Tratamiento.objects.get(id=id)
        if request.method == 'POST':
            tratamiento.delete()
            messages.success(request, '✅ Tratamiento eliminado exitosamente!')
            return redirect('crud:crud_tratamientos')
            
        return render(request, 'eliminar_tratamiento.html', {'tratamiento': tratamiento})
        
    except Tratamiento.DoesNotExist:
        messages.error(request, '❌ El tratamiento no existe.')
        return redirect('crud:crud_tratamientos')