from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
import json
from .models import Cliente, Producto, Venta, DetalleVenta
from .forms import ClienteForm, ProductoForm, VentaForm, DetalleVentaForm, RegistroForm
from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.contrib.auth.models import User
from .serializers import ClienteSerializer, ProductoSerializer, VentaSerializer
from rest_framework.viewsets import ModelViewSet


#Listar Cliente
@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'ventas/listar_clientes.html', {'clientes': clientes})

#Crear Cliente
@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'ventas/crear_cliente.html', {'form': form})

#Editar Cliente
@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'ventas/editar_cliente.html', {'form': form})

#Eliminar Cliente
@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'ventas/eliminar_cliente.html', {'cliente': cliente})

#Listar Productos
@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/listar_productos.html', {'productos': productos})

#Crear Producto
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'ventas/crear_producto.html', {'form': form})

#Editar Producto
@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'ventas/editar_producto.html', {'form': form})

#Eliminar Producto
@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'ventas/eliminar_producto.html', {'producto': producto})

#Listar Ventas
@login_required
def listar_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    datos = []

    for venta in ventas:
        detalles = DetalleVenta.objects.filter(venta=venta)

        total_sin_descuento = Decimal('0.00')
        total_cantidad = 0

        for d in detalles:
            subtotal = (d.precio * d.cantidad) - Decimal(str(d.descuento or 0))
            if subtotal < 0:
                subtotal = Decimal('0.00')
            total_sin_descuento += subtotal
            total_cantidad += d.cantidad

        if total_cantidad >= 10:
            porcentaje = Decimal('25')
        elif total_cantidad >= 5:
            porcentaje = Decimal('15')
        elif total_cantidad >= 3:
            porcentaje = Decimal('10')
        else:
            porcentaje = Decimal('0')

        descuento_global = (total_sin_descuento * (porcentaje / Decimal('100')))
        total_final = total_sin_descuento - descuento_global

        datos.append({
            "id": venta.id,
            "cliente": venta.cliente,
            "fecha": venta.fecha,
            "total_cantidad": total_cantidad,
            "porcentaje_descuento": int(porcentaje),
            "total_final": round(total_final, 2),
        })

    return render(request, "ventas/listar_ventas.html", {"ventas": datos})

#Crear Venta
@login_required
def crear_venta(request):
    VentaFormSet = inlineformset_factory(
        Venta,
        DetalleVenta,
        form=DetalleVentaForm,
        extra=1,
        can_delete=True
    )

    if request.method == "POST":
        venta_form = VentaForm(request.POST)
        formset = VentaFormSet(request.POST)

        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save()

            detalles = formset.save(commit=False)

            total_general = Decimal('0.00')
            total_cantidad = 0

            for detalle in detalles:
                detalle.venta = venta
                detalle.precio = detalle.producto.precio
                descuento_detalle = Decimal(str(detalle.descuento or 0))

                subtotal = (detalle.precio * detalle.cantidad) - descuento_detalle
                if subtotal < 0:
                    subtotal = Decimal('0.00')

                total_general += subtotal
                total_cantidad += detalle.cantidad

                detalle.save()

            # Eliminar objetos marcados para borrado (si aplica)
            for obj in formset.deleted_objects:
                obj.delete()

            # Descuento global (usar Decimal)
            if total_cantidad >= 10:
                descuento_global = Decimal('0.25')
            elif total_cantidad >= 5:
                descuento_global = Decimal('0.15')
            elif total_cantidad >= 3:
                descuento_global = Decimal('0.10')
            else:
                descuento_global = Decimal('0.00')

            total_final = total_general * (Decimal('1.00') - descuento_global)

            venta.total = total_final
            venta.save(update_fields=['total'])

            return redirect("listar_ventas")
    else:
        venta_form = VentaForm()
        formset = VentaFormSet()

    return render(request, "ventas/crear_venta.html", {
        "venta_form": venta_form,
        "formset": formset,
    })

#Editar Venta
@login_required
def editar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    VentaFormSet = inlineformset_factory(Venta, DetalleVenta, form=DetalleVentaForm, extra=0, can_delete=True)

    if request.method == 'POST':
        venta_form = VentaForm(request.POST, instance=venta)
        formset = VentaFormSet(request.POST, instance=venta)
        if venta_form.is_valid() and formset.is_valid():
            venta_form.save()
            detalles = formset.save(commit=False)

            total_general = Decimal('0.00')
            total_cantidad = 0

            for detalle in detalles:
                detalle.venta = venta
                detalle.precio = detalle.producto.precio
                subtotal = (detalle.precio * detalle.cantidad) - Decimal(str(detalle.descuento or 0))
                if subtotal < 0:
                    subtotal = Decimal('0.00')
                total_general += subtotal
                total_cantidad += detalle.cantidad
                detalle.save()

            for obj in formset.deleted_objects:
                obj.delete()

            # descuento global
            if total_cantidad >= 10:
                descuento_global = Decimal('0.25')
            elif total_cantidad >= 5:
                descuento_global = Decimal('0.15')
            elif total_cantidad >= 3:
                descuento_global = Decimal('0.10')
            else:
                descuento_global = Decimal('0.00')

            venta.total = total_general * (Decimal('1.00') - descuento_global)
            venta.save(update_fields=['total'])

            return redirect('listar_ventas')
    else:
        venta_form = VentaForm(instance=venta)
        formset = VentaFormSet(instance=venta)

    return render(request, 'ventas/editar_venta.html', {'venta_form': venta_form, 'formset': formset, 'venta': venta})

#Eliminar Venta
@login_required
def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('listar_ventas')
    return render(request, 'ventas/eliminar_venta.html', {'venta': venta})

#Detalles Venta
@login_required
def ver_detalles_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalleventa_set.all()

    total_sin_descuento = Decimal('0.00')
    total_cantidad = 0

    for d in detalles:
        subtotal = (d.precio * d.cantidad) - Decimal(str(d.descuento or 0))
        if subtotal < 0:
            subtotal = Decimal('0.00')
        total_sin_descuento += subtotal
        total_cantidad += d.cantidad

    if total_cantidad >= 10:
        porcentaje = Decimal('25')
    elif total_cantidad >= 5:
        porcentaje = Decimal('15')
    elif total_cantidad >= 3:
        porcentaje = Decimal('10')
    else:
        porcentaje = Decimal('0')

    descuento_global = (total_sin_descuento * (porcentaje / Decimal('100')))
    total_final = total_sin_descuento - descuento_global

    context = {
        'venta': venta,
        'detalles': detalles,
        'total_sin_descuento': round(total_sin_descuento, 2),
        'descuento_global': round(descuento_global, 2),
        'descuento_porcentaje': int(porcentaje),
        'total_final': round(total_final, 2),
        'total_cantidad': total_cantidad,
    }

    return render(request, 'ventas/ver_detalles_venta.html', context)

#Dashboard
@login_required
def dashboard(request):
    total_ventas = Venta.objects.count()
    total_clientes = Cliente.objects.count()
    total_productos = Producto.objects.count()

    productos_vendidos = (
        DetalleVenta.objects
        .values('producto__nombre')
        .exclude(producto__nombre=None)
        .annotate(total=Sum('cantidad'))
        .order_by('-total')[:5]
    )
    productos_labels = [p['producto__nombre'] for p in productos_vendidos]
    productos_data = [float(p['total']) for p in productos_vendidos]

    clientes_mas_compras = (
        Venta.objects
        .values('cliente__nombre')
        .exclude(cliente__nombre=None)
        .annotate(total=Sum('total'))
        .order_by('-total')[:5]
    )
    clientes_labels = [c['cliente__nombre'] for c in clientes_mas_compras]
    clientes_data = [float(c['total']) for c in clientes_mas_compras]

    context = {
        'total_ventas': total_ventas,
        'total_clientes': total_clientes,
        'total_productos': total_productos,
        'productos_labels': json.dumps(productos_labels),
        'productos_data': json.dumps(productos_data),
        'clientes_labels': json.dumps(clientes_labels),
        'clientes_data': json.dumps(clientes_data),
    }

    return render(request, 'dashboard.html', context)

#Registro Usuario
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password']
                    )

                    Cliente.objects.create(
                        user=user,
                        nombre=form.cleaned_data['username'],  # o agrega nombre al form si lo necesitas
                        rut=form.cleaned_data['rut'],
                        email=form.cleaned_data['email'],
                    )

                messages.success(request, "Usuario registrado exitosamente.")
                return redirect('login')

            except Exception as e:
                raise

        else:
            messages.error(request, "Corrige los errores del formulario.")

    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

def registro_exitoso(request):
        return render(request, 'registro_exitoso.html')

#Logout
@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('login.html')

#Para ver productos en crear venta
@login_required
def get_info_producto(request, id):
    producto = Producto.objects.get(id=id)
    return JsonResponse({
        "precio": float(producto.precio)
    })

#API ViewSets
class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class VentaViewSet(ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer