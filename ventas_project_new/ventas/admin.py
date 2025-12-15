from django.contrib import admin
import sys

print('admin.py: Intentando importar modelos...', file=sys.stderr)

try:
    from .models import Cliente
    print('admin.py: Cliente importado OK', file=sys.stderr)
    from .models import Producto
    print('admin.py: Producto importado OK', file=sys.stderr)
    from .models import Venta
    print('admin.py: Venta importado OK', file=sys.stderr)
    from .models import DetalleVenta
    print('admin.py: DetalleVenta importado OK', file=sys.stderr)
except Exception as e:
    # Print the import error to stderr but don't let admin autodiscover crash the process.
    print("Error importing ventas.models in admin.py:", e, file=sys.stderr)
else:
    # Cliente
    class ClienteAdmin(admin.ModelAdmin):
        list_display = ('id', 'nombre', 'email', 'rut', 'created_at', 'modified_at')
        search_fields = ('nombre', 'email', 'rut')
        list_filter = ('created_at', 'modified_at')
        ordering = ('id','-created_at')
    admin.site.register(Cliente, ClienteAdmin)

    # Producto
    class ProductoAdmin(admin.ModelAdmin):
        list_display = ('id', 'nombre', 'categoria', 'precio', 'created_at', 'modified_at')
        search_fields = ('nombre', 'categoria')
        list_filter = ('categoria', 'created_at', 'modified_at')
        ordering = ('id','-created_at')
    admin.site.register(Producto, ProductoAdmin)

    # Venta
    class VentaAdmin(admin.ModelAdmin):
        list_display = ('id', 'fecha', 'total', 'cliente', 'created_at', 'modified_at')
        search_fields = ('cliente__nombre', 'cliente__email', 'cliente__rut')
        list_filter = ('fecha', 'created_at', 'modified_at')
        ordering = ('id','-fecha')
    admin.site.register(Venta, VentaAdmin)

    # DetalleVenta
    class DetalleVentaAdmin(admin.ModelAdmin):
        list_display = ('id', 'producto', 'venta', 'precio', 'descuento', 'cantidad', 'created_at', 'modified_at')
        search_fields = ('producto__nombre', 'venta__uuid')
        list_filter = ('created_at', 'modified_at')
        ordering = ('id','-created_at')
    admin.site.register(DetalleVenta, DetalleVentaAdmin)