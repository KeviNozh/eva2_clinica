"""
URL configuration for salud_vital project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # API REST
    path('crud/', include('api.urls_crud')),  # CRUD Templates - CORREGIDO
    path('', TemplateView.as_view(template_name='index.html'), name='inicio'),
]