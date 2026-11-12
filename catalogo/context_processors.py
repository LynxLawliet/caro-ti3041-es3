from django.db import DatabaseError

from .models import ConsultaCliente
from .views import cargar_contenido


def contenido_sitio(request):
    url_name = getattr(request.resolver_match, 'url_name', '') or ''
    rutas_admin = {
        'admin_landing',
        'reporte_resumen',
        'reporte_critico',
        'crear_producto',
        'editar_producto',
        'admin_consultas',
        'responder_consulta',
        'eliminar_producto',
    }
    es_admin = bool(
        getattr(request.user, 'is_authenticated', False)
        and getattr(request.user, 'is_staff', False)
    )
    consultas_pendientes = 0
    if es_admin:
        try:
            consultas_pendientes = ConsultaCliente.objects.filter(respondida_en__isnull=True).count()
        except DatabaseError:
            consultas_pendientes = 0  # migración 0005 aún no aplicada
    return {
        'consultas_pendientes': consultas_pendientes,
        'contenido': cargar_contenido(),
        'es_admin': es_admin,
        'es_area_admin': es_admin and (url_name in rutas_admin),
        'url_actual': url_name,
    }

