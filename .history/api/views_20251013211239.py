# ========== PACIENTES CON FILTROS ==========
def crud_pacientes(request):
    pacientes = Paciente.objects.all()
    
    # Filtro por búsqueda de texto
    query = request.GET.get('q')
    if query:
        pacientes = pacientes.filter(
            models.Q(nombre__icontains=query) | 
            models.Q(apellido__icontains=query) |
            models.Q(rut__icontains=query)
        )
    
    # Filtro por género
    genero = request.GET.get('genero')
    if genero:
        pacientes = pacientes.filter(genero=genero)
    
    # Filtro por tipo de sangre
    tipo_sangre = request.GET.get('tipo_sangre')
    if tipo_sangre:
        pacientes = pacientes.filter(tipo_sangre=tipo_sangre)
    
    # Filtro por estado activo
    activo = request.GET.get('activo')
    if activo == 'true':
        pacientes = pacientes.filter(activo=True)
    elif activo == 'false':
        pacientes = pacientes.filter(activo=False)
    
    return render(request, 'crud_pacientes.html', {'pacientes': pacientes})