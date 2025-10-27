from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from decimal import Decimal
import uuid
import sys

print('models.py: Iniciando importación...', file=sys.stderr)

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

print('models.py: Cliente definido OK', file=sys.stderr)

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

print('models.py: Producto definido OK', file=sys.stderr)

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def actualizar_total(self):
        """Recalcula y guarda el total de la venta sumando los subtotales de sus detalles."""
        subtotal = self.detalleventa_set.aggregate(
            total=Sum(
                ExpressionWrapper(F('precio') * F('cantidad'),
                                  output_field=DecimalField(max_digits=10, decimal_places=2))
            )
        )['total'] or Decimal('0.00')
        self.total = subtotal
        # Guardar sólo el campo total
        self.save(update_fields=['total'])


    def __str__(self):
        return f"Venta {self.uuid} - {self.fecha.strftime('%d-%m-%Y')}"

print('models.py: Venta definido OK', file=sys.stderr)

class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)
    cantidad = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DetalleVenta {self.producto.nombre} x{self.cantidad}(Venta {self.venta.id})"

print('models.py: DetalleVenta definido OK', file=sys.stderr)