from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configuración de documentación con drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Sistema Salud Vital - API",
        default_version='v1',
        description="Documentación completa del API para el sistema de gestión médica",
        contact=openapi.Contact(email="admin@clinicavital.cl"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
# ... tus router.register() aquí ...

urlpatterns = [
    path('', include(router.urls)),
    
    # Documentación moderna
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-docs'),
]