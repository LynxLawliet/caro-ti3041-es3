from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('agregar/', views.crear_producto, name='crear_producto'),
    path('agregar-producto/', views.crear_producto, name='agregar_producto'),
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('reporte-resumen/', views.reporte_resumen, name='reporte_resumen'),
    path('reporte-critico/', views.reporte_critico, name='reporte_critico'),
    path('reportes/resumen/', views.reporte_resumen),
    path('reportes/critico/', views.reporte_critico),
    path('administracion/', views.admin_landing, name='admin_landing'),
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/actualizar/<int:producto_id>/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout, name='logout'),
    path('comprar/<int:producto_id>/', views.comprar, name='comprar'),
    path('pedido-confirmado/', views.pedido_confirmado, name='pedido_confirmado'),
    path('<int:producto_id>/', views.detalle, name='detalle'),
]