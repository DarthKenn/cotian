from django import forms
from .models import Producto, Venta

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock'] 
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
        
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad']

    total = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0)

    def clean_total(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        producto = cleaned_data.get('producto')

        if cantidad and producto:
            total = producto.precio * cantidad
            return total
        return 0