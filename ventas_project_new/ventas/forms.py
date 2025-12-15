from django import forms
from django.forms.widgets import Select
from django.forms import inlineformset_factory
from .models import Cliente, Producto, Venta, DetalleVenta
from django.contrib.auth.models import User

class ProductoSelect(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)

        # Convertir ModelChoiceIteratorValue → ID real
        if hasattr(value, "value"):
            real_value = value.value
        else:
            real_value = value

        if real_value:
            try:
                producto = Producto.objects.get(pk=real_value)
                option['attrs']['data-precio'] = float(producto.precio)
            except Producto.DoesNotExist:
                option['attrs']['data-precio'] = 0

        return option

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'rut']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': ProductoSelect(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('descuento'):
            self.initial['descuento'] = 0

DetalleVentaFormSet = inlineformset_factory(
    Venta,
    DetalleVenta,
    form=DetalleVentaForm,
    extra=1,
    can_delete=True
)

class RegistroForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nombre de usuario')
    email = forms.EmailField(label='Correo Electrónico')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')
    rut = forms.CharField(max_length=12, label='RUT')
    telefono = forms.CharField(max_length=20, label='Teléfono')

    # Validación: usuario repetido
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya existe.")
        return username

    # Validación: email repetido
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    # Validación: contraseñas coinciden
    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        cpwd = cleaned.get("confirm_password")

        if pwd and cpwd and pwd != cpwd:
            self.add_error("confirm_password", "Las contraseñas no coinciden.")

        return cleaned