"""
Vistas para la API del sistema Salud Vital
Endpoints REST para todos los modelos
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Especialidad, Sala, Medico, Paciente, Consulta, Medicamento, Tratamiento, Receta, SeguimientoPaciente
from .serializers import (
    EspecialidadSerializer, SalaSerializer, MedicoSerializer, 
    PacienteSerializer, ConsultaSerializer, MedicamentoSerializer,
    TratamientoSerializer, RecetaSerializer, SeguimientoPacienteSerializer
)
from .filters import MedicoFilter, PacienteFilter, ConsultaFilter

from django import forms
from django.shortcuts import render, redirect
from .models import Sala

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nombre', 'capacidad', 'tipo', 'descripcion', 'disponible']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

def crear_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_salas')  # Ajusta el nombre según tu URL
    else:
        form = SalaForm()
    
    return render(request, 'crear_sala.html', {'form': form})

def lista_salas(request):
    salas = Sala.objects.all()
    return render(request, 'lista_salas.html', {'salas': salas})

# VISTAS API (ViewSets)
class EspecialidadViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar especialidades médicas"""
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre']

class SalaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar salas de atención"""
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre', 'numero']
    filterset_fields = ['piso']

class MedicoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar médicos"""
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'especialidad__nombre']
    filterset_fields = ['especialidad']

class PacienteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar pacientes"""
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'apellido', 'rut', 'correo']
    filterset_fields = ['genero', 'tipo_sangre', 'activo']
    ordering_fields = ['fecha_registro', 'nombre', 'apellido']

class ConsultaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar consultas médicas"""
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paciente__nombre', 'medico__user__first_name', 'motivo']
    filterset_fields = ['estado', 'sala', 'medico']
    ordering_fields = ['fecha']

class MedicamentoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar medicamentos"""
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre', 'laboratorio']
    filterset_fields = ['tipo']

class TratamientoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar tratamientos"""
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['descripcion', 'consulta__paciente__nombre']

class RecetaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar recetas médicas"""
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['medicamento__nombre', 'consulta__paciente__nombre']

class SeguimientoPacienteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar seguimiento de pacientes"""
    queryset = SeguimientoPaciente.objects.all()
    serializer_class = SeguimientoPacienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paciente__nombre', 'medico__user__first_name', 'observaciones']
    filterset_fields = ['paciente', 'medico']
    ordering_fields = ['fecha_seguimiento']

# 🆕 VISTAS NORMALES PARA FORMULARIOS HTML
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Vistas para Especialidades
def crear_especialidad(request):
    if request.method == 'POST':
        try:
            Especialidad.objects.create(
                nombre=request.POST['nombre'],
                descripcion=request.POST.get('descripcion', '')
            )
            messages.success(request, "✅ Especialidad creada exitosamente!")
            return redirect('crud:crud_especialidades')
        except Exception as e:
            messages.error(request, f"❌ Error al crear especialidad: {str(e)}")
    return render(request, 'crear_especialidad.html')

def lista_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'crud_especialidades.html', {'especialidades': especialidades})

def eliminar_especialidad(request, id):
    especialidad = get_object_or_404(Especialidad, id=id)
    if request.method == 'POST':
        especialidad.delete()
        messages.success(request, "✅ Especialidad eliminada exitosamente!")
        return redirect('crud:crud_especialidades')
    return render(request, 'crud_especialidades.html')

# Vistas para Médicos
def crear_medico(request):
    especialidades = Especialidad.objects.all()
    if request.method == 'POST':
        try:
            Medico.objects.create(
                rut=request.POST['rut'],
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                especialidad_id=request.POST['especialidad'],
                telefono=request.POST.get('telefono', ''),
                correo=request.POST.get('correo', '')
            )
            messages.success(request, "✅ Médico creado exitosamente!")
            return redirect('crud:crud_medicos')
        except Exception as e:
            messages.error(request, f"❌ Error al crear médico: {str(e)}")
    return render(request, 'crear_medico.html', {'especialidades': especialidades})

def lista_medicos(request):
    medicos = Medico.objects.all()
    especialidades = Especialidad.objects.all()
    return render(request, 'crud_medicos.html', {
        'medicos': medicos,
        'especialidades': especialidades
    })

def editar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    especialidades = Especialidad.objects.all()
    if request.method == 'POST':
        try:
            medico.rut = request.POST['rut']
            medico.nombre = request.POST['nombre']
            medico.apellido = request.POST['apellido']
            medico.especialidad_id = request.POST['especialidad']
            medico.telefono = request.POST.get('telefono', '')
            medico.correo = request.POST.get('correo', '')
            medico.save()
            messages.success(request, "✅ Médico actualizado exitosamente!")
            return redirect('crud:crud_medicos')
        except Exception as e:
            messages.error(request, f"❌ Error al actualizar médico: {str(e)}")
    return render(request, 'editar_medico.html', {
        'medico': medico,
        'especialidades': especialidades
    })

def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        medico.delete()
        messages.success(request, "✅ Médico eliminado exitosamente!")
        return redirect('crud:crud_medicos')
    return render(request, 'eliminar_medico.html', {'medico': medico})

# Vistas para Pacientes
def crear_paciente(request):
    if request.method == 'POST':
        try:
            Paciente.objects.create(
                rut=request.POST['rut'],
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                fecha_nacimiento=request.POST['fecha_nacimiento'],
                genero=request.POST['genero'],
                tipo_sangre=request.POST['tipo_sangre'],
                telefono=request.POST.get('telefono', ''),
                correo=request.POST.get('correo', ''),
                direccion=request.POST.get('direccion', ''),
                activo=request.POST.get('activo') == 'on'
            )
            messages.success(request, "✅ Paciente creado exitosamente!")
            return redirect('crud:crud_pacientes')
        except Exception as e:
            messages.error(request, f"❌ Error al crear paciente: {str(e)}")
    return render(request, 'crear_paciente.html')

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'crud_pacientes.html', {'pacientes': pacientes})

def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        try:
            paciente.rut = request.POST['rut']
            paciente.nombre = request.POST['nombre']
            paciente.apellido = request.POST['apellido']
            paciente.fecha_nacimiento = request.POST['fecha_nacimiento']
            paciente.genero = request.POST['genero']
            paciente.tipo_sangre = request.POST['tipo_sangre']
            paciente.telefono = request.POST.get('telefono', '')
            paciente.correo = request.POST.get('correo', '')
            paciente.direccion = request.POST.get('direccion', '')
            paciente.activo = request.POST.get('activo') == 'on'
            paciente.save()
            messages.success(request, "✅ Paciente actualizado exitosamente!")
            return redirect('crud:crud_pacientes')
        except Exception as e:
            messages.error(request, f"❌ Error al actualizar paciente: {str(e)}")
    return render(request, 'editar_paciente.html', {'paciente': paciente})

def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, "✅ Paciente eliminado exitosamente!")
        return redirect('crud:crud_pacientes')
    return render(request, 'eliminar_paciente.html', {'paciente': paciente})

# Vistas para Medicamentos
def crear_medicamento(request):
    if request.method == 'POST':
        try:
            Medicamento.objects.create(
                nombre=request.POST['nombre'],
                laboratorio=request.POST.get('laboratorio', ''),
                stock=request.POST.get('stock', 0),
                precio_unitario=request.POST.get('precio_unitario', 0),
                tipo=request.POST.get('tipo', 'Tableta')
            )
            messages.success(request, "✅ Medicamento creado exitosamente!")
            return redirect('crud:crud_medicamentos')
        except Exception as e:
            messages.error(request, f"❌ Error al crear medicamento: {str(e)}")
    return render(request, 'crear_medicamento.html')

def lista_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    return render(request, 'crud_medicamentos.html', {'medicamentos': medicamentos})

def editar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        try:
            medicamento.nombre = request.POST['nombre']
            medicamento.laboratorio = request.POST.get('laboratorio', '')
            medicamento.stock = request.POST.get('stock', 0)
            medicamento.precio_unitario = request.POST.get('precio_unitario', 0)
            medicamento.tipo = request.POST.get('tipo', 'Tableta')
            medicamento.save()
            messages.success(request, "✅ Medicamento actualizado exitosamente!")
            return redirect('crud:crud_medicamentos')
        except Exception as e:
            messages.error(request, f"❌ Error al actualizar medicamento: {str(e)}")
    return render(request, 'editar_medicamento.html', {'medicamento': medicamento})

def eliminar_medicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        medicamento.delete()
        messages.success(request, "✅ Medicamento eliminado exitosamente!")
        return redirect('crud:crud_medicamentos')
    return render(request, 'eliminar_medicamento.html', {'medicamento': medicamento})

# Vistas para Consultas, Tratamientos, Recetas y Salas
def lista_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'crud_consultas.html', {'consultas': consultas})

def lista_tratamientos(request):
    tratamientos = Tratamiento.objects.all()
    return render(request, 'crud_tratamientos.html', {'tratamientos': tratamientos})

def lista_recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'crud_recetas.html', {'recetas': recetas})

def lista_salas(request):
    salas = Sala.objects.all()
    return render(request, 'crud_salas.html', {'salas': salas})

# Vistas para Consultas
def crear_consulta(request):
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    salas = Sala.objects.all()
    
    if request.method == 'POST':
        try:
            Consulta.objects.create(
                paciente_id=request.POST['paciente'],
                medico_id=request.POST['medico'],
                sala_id=request.POST.get('sala'),
                fecha=request.POST['fecha'],
                motivo=request.POST['motivo'],
                diagnostico=request.POST.get('diagnostico', ''),
                estado=request.POST.get('estado', 'programada')
            )
            messages.success(request, "✅ Consulta creada exitosamente!")
            return redirect('crud:crud_consultas')
        except Exception as e:
            messages.error(request, f"❌ Error al crear consulta: {str(e)}")
    
    return render(request, 'crear_consulta.html', {
        'pacientes': pacientes,
        'medicos': medicos,
        'salas': salas
    })

def lista_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'crud_consultas.html', {'consultas': consultas})

def editar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    salas = Sala.objects.all()
    
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
            messages.success(request, "✅ Consulta actualizada exitosamente!")
            return redirect('crud:crud_consultas')
        except Exception as e:
            messages.error(request, f"❌ Error al actualizar consulta: {str(e)}")
    
    return render(request, 'editar_consulta.html', {
        'consulta': consulta,
        'pacientes': pacientes,
        'medicos': medicos,
        'salas': salas
    })

def eliminar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, "✅ Consulta eliminada exitosamente!")
        return redirect('crud:crud_consultas')
    return render(request, 'eliminar_consulta.html', {'consulta': consulta})

# Vistas para Tratamientos
def crear_tratamiento(request):
    consultas = Consulta.objects.all()
    
    if request.method == 'POST':
        try:
            Tratamiento.objects.create(
                consulta_id=request.POST['consulta'],
                descripcion=request.POST['descripcion'],
                duracion_dias=request.POST.get('duracion_dias', 0),
                instrucciones=request.POST.get('instrucciones', '')
            )
            messages.success(request, "✅ Tratamiento creado exitosamente!")
            return redirect('crud:crud_tratamientos')
        except Exception as e:
            messages.error(request, f"❌ Error al crear tratamiento: {str(e)}")
    
    return render(request, 'crear_tratamiento.html', {'consultas': consultas})

def lista_tratamientos(request):
    tratamientos = Tratamiento.objects.all()
    return render(request, 'crud_tratamientos.html', {'tratamientos': tratamientos})

def editar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    consultas = Consulta.objects.all()
    
    if request.method == 'POST':
        try:
            tratamiento.consulta_id = request.POST['consulta']
            tratamiento.descripcion = request.POST['descripcion']
            tratamiento.duracion_dias = request.POST.get('duracion_dias', 0)
            tratamiento.instrucciones = request.POST.get('instrucciones', '')
            tratamiento.save()
            messages.success(request, "✅ Tratamiento actualizado exitosamente!")
            return redirect('crud:crud_tratamientos')
        except Exception as e:
            messages.error(request, f"❌ Error al actualizar tratamiento: {str(e)}")
    
    return render(request, 'editar_tratamiento.html', {
        'tratamiento': tratamiento,
        'consultas': consultas
    })

def eliminar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    if request.method == 'POST':
        tratamiento.delete()
        messages.success(request, "✅ Tratamiento eliminado exitosamente!")
        return redirect('crud:crud_tratamientos')
    return render(request, 'eliminar_tratamiento.html', {'tratamiento': tratamiento})

# Vistas para Salas
def crear_sala(request):
    if request.method == 'POST':
        try:
            Sala.objects.create(
                numero=request.POST['numero'],
                piso=request.POST.get('piso', 1),
                tipo=request.POST['tipo'],
                descripcion=request.POST.get('descripcion', ''),
                disponible=request.POST.get('disponible') == 'on'
            )
            messages.success(request, "✅ Sala creada exitosamente!")
            return redirect('crud:crud_salas')
        except Exception as e:
            messages.error(request, f"❌ Error al crear sala: {str(e)}")
    return render(request, 'crear_sala.html')

def lista_salas(request):
    salas = Sala.objects.all()
    return render(request, 'crud_salas.html', {'salas': salas})

def editar_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        try:
            sala.numero = request.POST['numero']
            sala.piso = request.POST.get('piso', 1)
            sala.tipo = request.POST['tipo']
            sala.descripcion = request.POST.get('descripcion', '')
            sala.disponible = request.POST.get('disponible') == 'on'
            sala.save()
            messages.success(request, "✅ Sala actualizada exitosamente!")
            return redirect('crud:crud_salas')
        except Exception as e:
            messages.error(request, f"❌ Error al actualizar sala: {str(e)}")
    return render(request, 'editar_sala.html', {'sala': sala})

def eliminar_sala(request, id):
    sala = get_object_or_404(Sala, id=id)
    if request.method == 'POST':
        sala.delete()
        messages.success(request, "✅ Sala eliminada exitosamente!")
        return redirect('crud:crud_salas')
    return render(request, 'eliminar_sala.html', {'sala': sala})