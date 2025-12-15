from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from decimal import Decimal
import uuid
from django.contrib.auth.models import User

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


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


class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def actualizar_total(self):
        subtotal = self.detalleventa_set.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('precio') * F('cantidad') - F('descuento'),
                    output_field=DecimalField(max_digits=12, decimal_places=2)
                )
            )
        )['total'] or Decimal('0.00')

        self.total = subtotal
        self.save(update_fields=['total'])

    def __str__(self):
        return f"Venta {self.uuid} - {self.fecha.strftime('%d-%m-%Y')}"


class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DetalleVenta {self.producto.nombre} x{self.cantidad} (Venta {self.venta.id})"

    @property
    def subtotal(self):
        return (self.cantidad * self.precio) - self.descuento
    
class Registro(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.username    
    
class RegistroExitoso(models.Model):
    id = models.AutoField(primary_key=True)
    mensaje = models.CharField(max_length=255, default="Registro exitoso. Ahora puedes iniciar sesión.")

    def __str__(self):
        return self.mensaje