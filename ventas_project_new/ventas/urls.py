from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    # Registro, Login y logout
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='root'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('registro/', views.registro_usuario,name='registro_usuario'),
    path('registro/success/', views.registro_exitoso, name='registro_exitoso'),
    
    # Dashboard (solo después del login)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Clientes
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),

    # Productos
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    # Ventas
    path('ventas/', views.listar_ventas, name='listar_ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('ventas/editar/<int:pk>/', views.editar_venta, name='editar_venta'),
    path('ventas/eliminar/<int:pk>/', views.eliminar_venta, name='eliminar_venta'),
    path('ventas/<int:venta_id>/detalles/', views.ver_detalles_venta, name='ver_detalles_venta'),

    #Para ver productos en crear venta
    path("producto/<int:id>/get_info/", views.get_info_producto, name="get_info_producto"),

    #API URLs
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

]