from django import forms
from .models import Cliente, Producto, Venta, DetalleVenta
from django.forms import inlineformset_factory

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'rut']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio']

class VentaForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        label='Producto'
    )
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Cantidad'
    )

    class Meta:
        model = Venta
        fields = ['cliente', 'producto', 'cantidad']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'descuento']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 1}),
            'descuento': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }

DetalleVentaFormSet = inlineformset_factory(
    Venta, DetalleVenta, form=DetalleVentaForm,
    fields=['producto', 'cantidad', 'descuento'],
    extra=1, can_delete=True
)