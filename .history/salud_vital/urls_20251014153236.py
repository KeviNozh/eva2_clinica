"""
URL configuration for salud_vital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URLS PRINCIPALES DEL PROYECTO EVA2_CLINICA
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # API REST
    path('crud/', include('api.urls_crud')),  # CRUD Templates FUNCIONALES
    path('', TemplateView.as_view(template_name='index.html'), name='inicio'),
    # Nuevas URLs para CRUD templates
    path('crud/especialidades/', TemplateView.as_view(template_name='crud_especialidades.html'), name='crud_especialidades'),
    path('crud/medicos/', TemplateView.as_view(template_name='crud_medicos.html'), name='crud_medicos'),
    path('crud/pacientes/', TemplateView.as_view(template_name='crud_pacientes.html'), name='crud_pacientes'),
    path('crud/consultas/', TemplateView.as_view(template_name='crud_consultas.html'), name='crud_consultas'),
    path('crud/medicamentos/', TemplateView.as_view(template_name='crud_medicamentos.html'), name='crud_medicamentos'),
    path('crud/tratamientos/', TemplateView.as_view(template_name='crud_tratamientos.html'), name='crud_tratamientos'),
    path('crud/recetas/', TemplateView.as_view(template_name='crud_recetas.html'), name='crud_recetas'),
    path('crud/salas/', TemplateView.as_view(template_name='crud_salas.html'), name='crud_salas'),
    path('crud/salas/', include('api.urls')),  # O donde tengas las URLs
]