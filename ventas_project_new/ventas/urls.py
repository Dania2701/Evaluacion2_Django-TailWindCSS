from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    # Rutas para productos y ventas (si se quieren exponer en la app)
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('ventas/', views.listar_ventas, name='listar_ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('ventas/editar/<int:pk>/', views.editar_venta, name='editar_venta'),
    path('ventas/eliminar/<int:pk>/', views.eliminar_venta, name='eliminar_venta'),
    path('ventas/<int:venta_id>/detalles/', views.ver_detalles_venta, name='ver_detalles_venta'),
]
