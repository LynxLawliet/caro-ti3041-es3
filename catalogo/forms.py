from django import forms
from django.core.validators import validate_email
from .models import Categoria, ConsultaCliente, Producto


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


class ConsultaClienteForm(forms.ModelForm):
    """
    Formulario vinculado a ConsultaCliente para canalizar dudas,
    cotizaciones y requerimientos técnicos de los clientes.
    """
    class Meta:
        model = ConsultaCliente
        fields = [
            'nombre',
            'correo',
            'producto_interes',
            'mensaje',
        ]
        labels = {
            'nombre': 'Nombre completo',
            'correo': 'Correo electrónico',
            'producto_interes': 'Producto de interés (opcional)',
            'mensaje': 'Consulta o requerimiento técnico',
        }
        help_texts = {
            'correo': 'Te responderemos a esta dirección de correo a la brevedad.',
            'producto_interes': 'Selecciona el artículo si deseas consultar disponibilidad o ficha técnica.',
            'mensaje': 'Describe tu duda o requerimiento técnico (mínimo 10 caracteres).',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Ej. Carlos Miranda Lagos',
                'autocomplete': 'name',
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'campo-formulario',
                'placeholder': 'ejemplo@correo.cl',
                'autocomplete': 'email',
            }),
            'producto_interes': forms.Select(attrs={
                'class': 'campo-formulario campo-select',
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'campo-formulario campo-textarea',
                'rows': 5,
                'placeholder': 'Escribe aquí tu consulta o requerimiento técnico...',
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre no puede estar vacío.')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        return nombre

    def clean_correo(self):
        correo = self.cleaned_data.get('correo', '').strip()
        if not correo:
            raise forms.ValidationError('El correo electrónico es obligatorio.')
        try:
            validate_email(correo)
        except forms.ValidationError:
            raise forms.ValidationError('Por favor ingresa un correo electrónico con formato válido.')
        return correo

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje', '').strip()
        if not mensaje:
            raise forms.ValidationError('El mensaje no puede estar vacío.')
        if len(mensaje) < 10:
            raise forms.ValidationError('El mensaje debe contener al menos 10 caracteres para procesar tu solicitud.')
        return mensaje


class RespuestaConsultaForm(forms.Form):
    """Respuesta del administrador a una consulta técnica de un cliente."""
    respuesta = forms.CharField(
        label='Respuesta al cliente',
        min_length=10,
        max_length=4000,
        help_text='Se enviará al correo del cliente y quedará guardada en la consulta (mínimo 10 caracteres).',
        widget=forms.Textarea(attrs={
            'class': 'campo-formulario campo-textarea',
            'rows': 8,
            'placeholder': 'Escribe aquí la respuesta técnica...',
        }),
    )
