from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
import json
from .models import Cliente, Producto, Venta, DetalleVenta
from .forms import ClienteForm, ProductoForm, VentaForm, DetalleVentaForm

#Listar Cliente
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'ventas/listar_clientes.html', {'clientes': clientes})

#Crear Cliente
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
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'ventas/eliminar_cliente.html', {'cliente': cliente})

#Listar Productos
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/listar_productos.html', {'productos': productos})

#Crear Producto
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
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'ventas/eliminar_producto.html', {'producto': producto})

#Listar Ventas
def listar_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/listar_ventas.html', {'ventas': ventas})

#Crear Venta
def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save()
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            
            # Crear el detalle de venta
            precio = producto.precio
            
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio=precio
            )
            
            # Recalcular y guardar el total de la venta
            venta.actualizar_total()
            
            return redirect('listar_ventas')
    else:
        form = VentaForm()
    return render(request, 'ventas/crear_venta.html', {'form': form})

#Editar Venta
def editar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('listar_ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'ventas/editar_venta.html', {'form': form})

#Eliminar Venta
def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('listar_ventas')
    return render(request, 'ventas/eliminar_venta.html', {'venta': venta})

# Ver detalles de una venta
def ver_detalles_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    detalles = venta.detalleventa_set.all()
    return render(request, 'ventas/ver_detalles_venta.html', {
        'venta': venta,
        'detalles': detalles
    })
