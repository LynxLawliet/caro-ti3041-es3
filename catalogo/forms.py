from django import forms
from .models import Categoria, Producto


class ProductoForm(forms.ModelForm):
    """
    Formulario vinculado al modelo Producto para la gestión y validación
    de altas y modificaciones en el catálogo de Ferretería Caro-Kahn.
    """
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'categoria',
            'precio',
            'stock',
            'imagen_url',
            'descripcion',
            'visible',
        ]
        labels = {
            'nombre': 'Nombre del producto',
            'categoria': 'Categoría',
            'precio': 'Precio ($CLP)',
            'stock': 'Stock disponible',
            'imagen_url': 'URL de imagen (opcional)',
            'descripcion': 'Descripción técnica',
            'visible': 'Visible en catálogo público',
        }
        help_texts = {
            'precio': 'Ingresa el valor en pesos chilenos (sin decimales ni signos).',
            'stock': 'Cantidad de unidades en inventario para venta o cotización.',
            'imagen_url': 'Enlace público directo (JPG, PNG o WebP).',
            'visible': 'Desmarca esta casilla para ocultar el producto del catálogo público.',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Ej. Martillo de carpintero 16 oz',
                'autocomplete': 'off',
            }),
            'categoria': forms.Select(attrs={
                'class': 'campo-formulario campo-select',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Ej. 5990',
                'min': '0',
                'step': '1',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Ej. 15',
                'min': '0',
                'step': '1',
            }),
            'imagen_url': forms.URLInput(attrs={
                'class': 'campo-formulario',
                'placeholder': 'https://...',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'campo-formulario campo-textarea',
                'rows': 4,
                'placeholder': 'Especificaciones técnicas, medidas, composición o usos recomendados...',
            }),
            'visible': forms.CheckboxInput(attrs={
                'class': 'campo-checkbox',
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre del producto no puede estar vacío.')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe contener al menos 3 caracteres.')
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is None or precio < 0:
            raise forms.ValidationError('El precio debe ser un número entero mayor o igual a 0.')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None or stock < 0:
            raise forms.ValidationError('El stock no puede ser un valor negativo.')
        return stock
