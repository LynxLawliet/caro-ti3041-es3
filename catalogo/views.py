from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Avg, Count, Max, Min, Sum
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from .forms import ConsultaClienteForm, ProductoForm, RespuestaConsultaForm
from .models import (
    Categoria,
    ConsultaCliente,
    ContenidoSitio,
    Pedido,
    Producto,
    RegistroAdministrativo,
)

CATEGORIA_VISUAL = {
    "herramientas-manuales": "🔨",
    "herramientas-electricas": "⚡",
    "accesorios-para-herramientas": "⚙",
    "abrasivos": "◈",
    "fijaciones": "⊕",
    "medicion": "📏",
    "refuerzo-de-taludes": "⛰",
    "geosinteticos": "▦",
    "acero-para-hormigon": "▤",
    "mezclas-asfalticas": "▰",
    "equipos-para-obra-civil": "⚒",
    "iluminacion": "✦",
    "adhesivos-y-sellantes": "◉",
    "plomeria": "◌",
    "seguridad-industrial": "⛑",
}

CONTENIDO_POR_DEFECTO = {
    'marca': 'Ferretería Caro-Kahn',
    'home_etiqueta': 'Todo para obra, hogar y mantenimiento',
    'home_titulo': 'Materiales y herramientas que impulsan cada proyecto.',
    'home_descripcion': 'Desde herramientas manuales hasta materiales para construcción, en Ferretería Caro-Kahn encontrarás soluciones confiables para obra, remodelación y mantenimiento diario.',
    'home_cta': 'Explorar catálogo',
    'catalogo_etiqueta': 'Soluciones para tus proyectos',
    'catalogo_titulo': 'Nuestro catálogo técnico',
    'catalogo_descripcion': 'Encuentra herramientas, materiales y accesorios para cada trabajo.',
    'home_beneficios_etiqueta': '¿Por qué elegirnos?',
    'home_beneficios_titulo': 'Más que herramientas, soluciones para cada trabajo.',
    'beneficio_1_titulo': 'Amplio stock',
    'beneficio_1_descripcion': 'Disponibilidad para obra, mantenimiento y uso doméstico.',
    'beneficio_2_titulo': 'Calidad profesional',
    'beneficio_2_descripcion': 'Productos pensados para un uso frecuente y exigente.',
    'beneficio_3_titulo': 'Compra rápida',
    'beneficio_3_descripcion': 'Proceso simple para comparar, agregar y confirmar compras.',
    'home_cta_etiqueta': 'Tu proyecto empieza aquí',
    'home_cta_titulo': 'Encuentra lo que necesitas para construir con confianza.',
    'lista_hero_titulo': 'Materiales y soluciones profesionales para tus proyectos',
    'lista_hero_descripcion': 'Encuentra herramientas, materiales y accesorios con información clara de stock, precios y compra directa.',
    'lista_testimonios_titulo': 'Una compra pensada para profesionales',
    'testimonio_1_texto': 'Encontrar el producto, revisar el stock y agregarlo al carrito es rápido y claro.',
    'testimonio_1_autor': 'Cliente de obra',
    'testimonio_1_rol': 'Compras para construcción',
    'testimonio_2_texto': 'La información del catálogo ayuda a comparar opciones antes de tomar una decisión.',
    'testimonio_2_autor': 'Profesional independiente',
    'testimonio_2_rol': 'Herramientas y mantenimiento',
    'lista_cta_titulo': '¿Listo para empezar tu próximo proyecto?',
    'lista_cta_descripcion': 'Selecciona tus productos, revisa tu carrito y completa tu compra.',
    'footer_descripcion': 'Tu aliado estratégico en materiales y soluciones de construcción profesional.',
}

def index(request):
    productos = _productos_disponibles()
    destacados = productos[:4]
    conteo_categorias = {}
    for producto in productos:
        nombre = producto['categoria'].strip()
        conteo_categorias[nombre] = conteo_categorias.get(nombre, 0) + 1

    categorias = []
    for nombre, cantidad in sorted(
        conteo_categorias.items(),
        key=lambda categoria: categoria[0].casefold(),
    ):
        estilo = slugify(nombre)
        icono = CATEGORIA_VISUAL.get(estilo, "✳")
        categorias.append({
            "nombre": nombre,
            "cantidad": cantidad,
            "estilo": estilo if estilo in CATEGORIA_VISUAL else "general",
            "icono": icono,
        })

    # Carrusel: variedad de categorías (rotando una por categoría, máx. 8)
    por_categoria = {}
    for producto in productos:
        por_categoria.setdefault(producto['categoria'].strip(), []).append(producto)
    carrusel = []
    ronda = 0
    while len(carrusel) < 8 and any(len(lista_cat) > ronda for lista_cat in por_categoria.values()):
        for lista_cat in por_categoria.values():
            if len(lista_cat) > ronda and len(carrusel) < 8:
                carrusel.append(lista_cat[ronda])
        ronda += 1

    contexto = {
        'productos_destacados': destacados,
        'productos_carrusel': carrusel,
        'categorias': categorias,
        'total_productos': len(productos),
    }
    return render(request, 'catalogo/home.html', contexto)

def cargar_contenido():
    contenido_sitio = {
        registro.clave: registro.valor
        for registro in ContenidoSitio.objects.all()
    }
    return {**CONTENIDO_POR_DEFECTO, **contenido_sitio}


def _producto_a_dict(producto):
    return {
        'id': producto.pk,
        'nombre': producto.nombre,
        'categoria': producto.categoria.nombre,
        'precio': int(producto.precio),
        'stock': producto.stock,
        'imagen_url': producto.imagen_url,
        'imagen_archivo': producto.imagen_archivo,
        'descripcion': producto.descripcion,
        'visible': producto.visible,
    }


def _productos_disponibles():
    return [
        _producto_a_dict(producto)
        for producto in Producto.objects.filter(visible=True)
        .select_related('categoria')
        .order_by('pk')
    ]

def lista(request):
    productos = _productos_disponibles()
    busqueda = request.GET.get('q', request.GET.get('nombre', '')).strip()
    categoria_seleccionada = request.GET.get('categoria', '').strip()

    if busqueda:
        texto_busqueda = busqueda.casefold()
        productos = [
            producto for producto in productos
            if texto_busqueda in producto['nombre'].casefold()
        ]

    if categoria_seleccionada:
        categoria_normalizada = categoria_seleccionada.casefold()
        productos = [
            producto for producto in productos
            if producto['categoria'].casefold() == categoria_normalizada
        ]

    # Cálculos para el resumen
    todos_los_productos = _productos_disponibles()
    total_registros = len(productos)
    productos_con_stock = sum(1 for p in productos if p['stock'] > 0)
    categorias = sorted({p['categoria'] for p in todos_los_productos})
    
    contexto = {
        'productos': productos,
        'total_registros': total_registros,
        'productos_con_stock': productos_con_stock,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_seleccionada': categoria_seleccionada,
    }
    return render(request, 'catalogo/lista.html', contexto)

def admin_landing(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Debes iniciar sesión con una cuenta administradora.')
        return redirect(f"{reverse('login')}?next={reverse('admin_landing')}")

    productos = [
        _producto_a_dict(producto)
        for producto in Producto.objects.select_related('categoria').order_by('pk')
    ]
    contenido = cargar_contenido()
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'guardar_contenido':
            campos = CONTENIDO_POR_DEFECTO.keys()
            contenido.update({campo: request.POST.get(campo, contenido.get(campo, '')) for campo in campos})
            for campo in campos:
                ContenidoSitio.objects.update_or_create(
                    clave=campo,
                    defaults={
                        'valor': contenido[campo],
                        'actualizado_por': request.user,
                    },
                )
            RegistroAdministrativo.registrar(
                usuario=request.user,
                accion=RegistroAdministrativo.Accion.ACTUALIZACION,
                modelo="ContenidoSitio",
                resumen="Se actualizaron los textos visibles de la página.",
            )
            messages.success(request, 'Los textos visibles de la Landingpage fueron actualizados.')
        elif accion == 'guardar_producto':
            try:
                producto_id = int(request.POST.get('producto_id', ''))
                producto = Producto.objects.get(pk=producto_id)
                nombre = request.POST.get('nombre', '').strip()
                categoria_nombre = request.POST.get('categoria', '').strip()
                stock = int(request.POST.get('stock', '0'))
                precio = int(request.POST.get('precio', producto.precio))
                if not nombre or not categoria_nombre:
                    raise ValueError
                if stock < 0 or precio < 0:
                    raise ValueError
                with transaction.atomic():
                    categoria, _ = Categoria.objects.get_or_create(nombre=categoria_nombre)
                    producto.nombre = nombre
                    producto.categoria = categoria
                    producto.descripcion = request.POST.get('descripcion', '').strip()
                    producto.imagen_url = request.POST.get('imagen_url', '').strip()
                    producto.precio = precio
                    producto.stock = stock
                    producto.visible = request.POST.get('visible') == 'on'
                    producto.full_clean()
                    producto.save()
                RegistroAdministrativo.registrar(
                    usuario=request.user,
                    accion=RegistroAdministrativo.Accion.ACTUALIZACION,
                    modelo="Producto",
                    objeto_id=producto_id,
                    resumen=f'Se actualizó el producto "{producto.nombre}".',
                )
                messages.success(request, f'El producto "{producto.nombre}" fue actualizado.')
            except (Producto.DoesNotExist, TypeError, ValueError, ValidationError):
                messages.error(request, 'No se pudo actualizar el producto. Revisa los campos.')
        elif accion == 'crear_producto':
            try:
                nombre = request.POST.get('nombre', '').strip()
                categoria_nombre = request.POST.get('categoria', '').strip()
                precio = int(request.POST.get('precio', '0'))
                stock = int(request.POST.get('stock', '0'))
                if not nombre or not categoria_nombre or precio < 0 or stock < 0:
                    raise ValueError
                with transaction.atomic():
                    categoria, _ = Categoria.objects.get_or_create(nombre=categoria_nombre)
                    producto = Producto(
                        nombre=nombre,
                        categoria=categoria,
                        precio=precio,
                        stock=stock,
                        imagen_url=request.POST.get('imagen_url', '').strip(),
                        descripcion=request.POST.get('descripcion', '').strip(),
                        visible=request.POST.get('visible') == 'on',
                    )
                    producto.full_clean()
                    producto.save()
                RegistroAdministrativo.registrar(
                    usuario=request.user,
                    accion=RegistroAdministrativo.Accion.CREACION,
                    modelo="Producto",
                    objeto_id=producto.pk,
                    resumen=f'Se añadió el producto "{nombre}" al catálogo.',
                )
                messages.success(request, f'El producto "{nombre}" fue añadido al catálogo.')
            except (TypeError, ValueError, ValidationError):
                messages.error(request, 'No se pudo añadir el producto. Revisa nombre, precio y stock.')
        elif accion == 'eliminar_producto':
            try:
                producto_id = int(request.POST.get('producto_id', ''))
                producto = Producto.objects.get(pk=producto_id)
                nombre = producto.nombre
                producto.delete()
                carrito = request.session.get('carrito', {})
                carrito.pop(str(producto_id), None)
                request.session['carrito'] = carrito
                request.session.modified = True
                RegistroAdministrativo.registrar(
                    usuario=request.user,
                    accion=RegistroAdministrativo.Accion.ELIMINACION,
                    modelo="Producto",
                    objeto_id=producto_id,
                    resumen=f'Se eliminó el producto "{nombre}" del catálogo.',
                )
                messages.success(request, f'El producto "{nombre}" fue eliminado del catálogo.')
            except (Producto.DoesNotExist, TypeError, ValueError):
                messages.error(request, 'No se pudo eliminar el producto seleccionado.')

    productos = [
        _producto_a_dict(producto)
        for producto in Producto.objects.select_related('categoria').order_by('pk')
    ]
    contenido = cargar_contenido()
    kpis = {
        'total_productos': len(productos),
        'total_criticos': sum(1 for p in productos if p['stock'] <= 5),
        'total_agotados': sum(1 for p in productos if p['stock'] == 0),
        'total_visibles': sum(1 for p in productos if p.get('visible')),
    }
    return render(request, 'catalogo/admin_landing.html', {
        'productos': productos,
        'contenido': contenido,
        'kpis': kpis,
    })

def detalle(request, producto_id):
    productos = _productos_disponibles()
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if not producto:
        raise Http404("Producto no encontrado en la ferretería")

    # Registrar en sesión los últimos 3 productos visualizados
    ultimos_vistos = request.session.get('ultimos_vistos', [])
    if producto_id in ultimos_vistos:
        ultimos_vistos.remove(producto_id)
    ultimos_vistos.insert(0, producto_id)
    request.session['ultimos_vistos'] = ultimos_vistos[:3]
    request.session.modified = True

    return render(request, 'catalogo/detalle.html', {'producto': producto})


def _obtener_carrito(request):
    return request.session.get('carrito', {})


def _guardar_carrito(request, carrito):
    request.session['carrito'] = carrito
    request.session.modified = True


def agregar_al_carrito(request, producto_id):
    if request.method != 'POST':
        return redirect('detalle', producto_id=producto_id)

    producto = next(
        (producto for producto in _productos_disponibles() if producto['id'] == producto_id),
        None,
    )
    if not producto:
        raise Http404('Producto no encontrado en la ferretería')
    if producto['stock'] <= 0:
        messages.error(request, 'Este producto no tiene stock disponible.')
        return redirect('detalle', producto_id=producto_id)

    try:
        cantidad_solicitada = int(request.POST.get('cantidad', ''))
    except (TypeError, ValueError):
        cantidad_solicitada = 0

    if cantidad_solicitada < 1:
        messages.error(request, 'Ingresa una cantidad entera de al menos 1.')
        return redirect('detalle', producto_id=producto_id)

    carrito = _obtener_carrito(request)
    clave_producto = str(producto_id)
    item_existente = carrito.get(clave_producto, {})
    try:
        cantidad_existente = int(item_existente.get('cantidad', 0))
    except (TypeError, ValueError):
        messages.error(request, 'No se pudo validar la cantidad que ya está en el carrito.')
        return redirect('carrito')

    if cantidad_existente < 0:
        messages.error(request, 'No se pudo validar la cantidad que ya está en el carrito.')
        return redirect('carrito')

    cantidad_total = cantidad_existente + cantidad_solicitada
    if cantidad_total <= producto['stock']:
        carrito[clave_producto] = {
            'id': producto['id'],
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'cantidad': cantidad_total,
            'imagen_url': producto.get('imagen_url', ''),
        }
        _guardar_carrito(request, carrito)
        messages.success(request, f"Se añadieron {cantidad_solicitada} unidad(es) de {producto['nombre']} al carrito.")
        return redirect('carrito')
    else:
        disponibles = max(producto['stock'] - cantidad_existente, 0)
        messages.warning(request, f'Solo puedes añadir {disponibles} unidad(es) más de este producto.')
    return redirect('detalle', producto_id=producto_id)


def carrito(request):
    items = _items_con_subtotales(request)
    total = sum(item['subtotal'] for item in items)
    return render(request, 'catalogo/carrito.html', {'items_carrito': items, 'total_carrito': total})


def _items_con_subtotales(request):
    items = []
    for item in _obtener_carrito(request).values():
        item_con_subtotal = dict(item)
        item_con_subtotal['subtotal'] = item['precio'] * item['cantidad']
        items.append(item_con_subtotal)
    return items


def vaciar_carrito(request):
    if request.method == 'POST':
        request.session.pop('carrito', None)
        messages.success(request, 'El carrito temporal fue vaciado.')
    return redirect('carrito')


def actualizar_cantidad_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = _obtener_carrito(request)
        clave_producto = str(producto_id)
        if clave_producto not in carrito:
            messages.error(request, 'El producto no está en el carrito.')
            return redirect('carrito')

        producto = next(
            (producto for producto in _productos_disponibles() if producto['id'] == producto_id),
            None,
        )
        try:
            cantidad = int(request.POST.get('cantidad', 0))
        except (TypeError, ValueError):
            cantidad = 0

        if cantidad <= 0:
            carrito.pop(clave_producto, None)
            _guardar_carrito(request, carrito)
            messages.info(request, 'Producto eliminado del carrito.')
        elif not producto:
            messages.error(request, 'Producto no encontrado en la ferretería.')
        elif cantidad > producto['stock']:
            messages.warning(request, f"Solo hay {producto['stock']} unidad(es) disponibles.")
        else:
            carrito[clave_producto]['cantidad'] = cantidad
            _guardar_carrito(request, carrito)
            messages.success(request, 'Cantidad actualizada.')
    return redirect('carrito')


def eliminar_del_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = _obtener_carrito(request)
        if carrito.pop(str(producto_id), None) is not None:
            _guardar_carrito(request, carrito)
            messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito')


def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '').strip()
        contrasena = request.POST.get('contrasena', '')
        usuario_django = authenticate(request, username=usuario, password=contrasena)
        if usuario_django and usuario_django.is_staff:
            auth_login(request, usuario_django)
            request.session['usuario_ficticio'] = usuario_django.get_username()
            messages.success(request, f'Bienvenido/a, {usuario_django.get_username()}.')
            return redirect(request.POST.get('next') or 'admin_landing')

        usuario_registrado = request.session.get('usuario_registrado')
        if (
            usuario
            and usuario_registrado
            and usuario == usuario_registrado.get('usuario')
            and contrasena == usuario_registrado.get('contrasena')
        ):
            request.session['usuario_ficticio'] = usuario
            messages.success(request, f'Bienvenido/a, {usuario}.')
            return redirect(request.POST.get('next') or 'carrito')
        messages.error(request, 'El usuario o la contraseña no son válidos.')
    return render(request, 'catalogo/login.html', {'modo': 'login'})


def registro(request):
    valores = {}
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '').strip()
        correo = request.POST.get('correo', '').strip()
        contrasena = request.POST.get('contrasena', '')
        confirmacion = request.POST.get('confirmacion', '')
        valores = {'usuario': usuario, 'correo': correo}
        correo_valido = True
        if correo:
            try:
                validate_email(correo)
            except ValidationError:
                correo_valido = False
        if not usuario or not contrasena:
            messages.error(request, 'Completa el usuario y la contraseña.')
        elif not correo:
            messages.error(request, 'Ingresa tu correo electrónico.')
        elif not correo_valido:
            messages.error(request, 'Ingresa un correo electrónico válido (ej. nombre@correo.cl).')
        elif contrasena != confirmacion:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            request.session['usuario_registrado'] = {
                'usuario': usuario,
                'correo': correo,
                'contrasena': contrasena,
            }
            request.session['usuario_ficticio'] = usuario
            messages.success(request, f'Cuenta simulada creada para {usuario}.')
            return redirect(request.POST.get('next') or 'lista')
    return render(request, 'catalogo/login.html', {'modo': 'registro', 'valores': valores})


def logout(request):
    auth_logout(request)
    request.session.pop('usuario_ficticio', None)
    messages.success(request, 'La sesión simulada fue cerrada.')
    return redirect('lista')


def comprar(request, producto_id):
    if not request.session.get('usuario_ficticio'):
        messages.info(request, 'Inicia sesión para comprar este producto.')
        return redirect(f"{reverse('login')}?next={reverse('comprar', args=[producto_id])}")

    if request.method != 'POST':
        return redirect('detalle', producto_id=producto_id)

    producto = next(
        (producto for producto in _productos_disponibles() if producto['id'] == producto_id),
        None,
    )
    if not producto:
        raise Http404('Producto no encontrado en la ferretería')
    if producto['stock'] <= 0:
        messages.error(request, 'Este producto no tiene stock disponible.')
        return redirect('lista')

    try:
        cantidad = int(request.POST.get('cantidad', ''))
    except (TypeError, ValueError):
        cantidad = 0
    if cantidad < 1:
        messages.error(request, 'Ingresa una cantidad entera de al menos 1.')
        return redirect('detalle', producto_id=producto_id)
    if cantidad > producto['stock']:
        messages.warning(request, f"Solo hay {producto['stock']} unidad(es) disponibles.")
        return redirect('detalle', producto_id=producto_id)

    carrito = _obtener_carrito(request)
    carrito[str(producto_id)] = {
        'id': producto['id'],
        'nombre': producto['nombre'],
        'precio': producto['precio'],
        'cantidad': cantidad,
        'imagen_url': producto.get('imagen_url', ''),
    }
    _guardar_carrito(request, carrito)
    messages.success(request, f"{cantidad} unidad(es) de {producto['nombre']} lista(s) para finalizar la compra.")
    return redirect('checkout')


def pedido_confirmado(request):
    items = request.session.get('ultimo_pedido', [])
    total = sum(item['subtotal'] for item in items)
    return render(request, 'catalogo/pedido_confirmado.html', {
        'items_carrito': items,
        'total_carrito': total,
    })


def checkout(request):
    if not request.session.get('usuario_ficticio'):
        messages.info(request, 'Inicia sesión para finalizar la compra simulada.')
        return redirect(f"{reverse('login')}?next={reverse('checkout')}")

    items = _items_con_subtotales(request)
    if not items:
        messages.info(request, 'Tu carrito está vacío.')
        return redirect('carrito')

    total = sum(item['subtotal'] for item in items)
    if request.method == 'POST':
        usuario = request.user if request.user.is_authenticated else None
        with transaction.atomic():
            productos = {
                producto.pk: producto
                for producto in Producto.objects.filter(
                    pk__in=[item['id'] for item in items],
                    visible=True,
                ).select_for_update()
            }
            for item in items:
                producto = productos.get(item['id'])
                if producto is None or item['cantidad'] > producto.stock:
                    messages.error(
                        request,
                        f"El stock de {item['nombre']} cambió y ya no alcanza para completar el pedido.",
                    )
                    return redirect('carrito')

            for item in items:
                producto = productos[item['id']]
                producto.stock -= item['cantidad']
                producto.save(update_fields=('stock', 'actualizado_en'))

            Pedido.registrar_compra(
                items,
                nombre_cliente=request.session['usuario_ficticio'],
                usuario=usuario,
            )

        request.session['ultimo_pedido'] = items
        request.session.pop('carrito', None)
        messages.success(request, 'Pedido confirmado correctamente (simulación).')
        return redirect('pedido_confirmado')

    return render(request, 'catalogo/checkout.html', {'items_carrito': items, 'total_carrito': total})


def _es_administrador(request):
    """Verifica si el usuario actual posee permisos de staff/administrador."""
    return getattr(request.user, 'is_authenticated', False) and getattr(request.user, 'is_staff', False)


def crear_producto(request):
    """
    Vista para crear un nuevo registro instanciando el formulario vacío.
    Restringida exclusivamente a usuarios con rol de administrador (staff).
    Tras guardarse exitosamente con POST, redirige a la vista del listado principal.
    """
    if not _es_administrador(request):
        messages.error(request, 'Acceso restringido: Se requieren permisos de administrador para agregar productos.')
        return redirect('lista')

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" agregado exitosamente.')
            return redirect('lista')
    else:
        form = ProductoForm()

    contexto = {
        'form': form,
        'modo': 'crear',
        'titulo_accion': 'Agregar nuevo producto',
        'subtitulo_accion': 'Completa el formulario para registrar un nuevo material o herramienta en el catálogo técnico.',
        'boton_texto': 'Guardar producto',
        'contenido': cargar_contenido(),
    }
    return render(request, 'catalogo/formulario_producto.html', contexto)


def editar_producto(request, id):
    """
    Vista para editar un registro existente pasando la instancia específica
    (identificada por su ID) al formulario.
    Restringida exclusivamente a usuarios con rol de administrador (staff).
    Tras guardarse exitosamente con POST, redirige a la vista del listado principal.
    """
    if not _es_administrador(request):
        messages.error(request, 'Acceso restringido: Se requieren permisos de administrador para editar productos.')
        return redirect('lista')

    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('lista')
    else:
        form = ProductoForm(instance=producto)

    contexto = {
        'form': form,
        'producto': producto,
        'modo': 'editar',
        'titulo_accion': f'Editar producto: {producto.nombre}',
        'subtitulo_accion': 'Modifica los valores del producto y confirma los cambios para actualizar el inventario.',
        'boton_texto': 'Guardar cambios',
        'contenido': cargar_contenido(),
    }
    return render(request, 'catalogo/formulario_producto.html', contexto)


def eliminar_producto(request, id):
    """
    Vista para eliminar el objeto de la base de datos previa confirmación.
    Restringida exclusivamente a usuarios con rol de administrador (staff).
    Tras confirmarse exitosamente con POST, redirige a la vista del listado principal.
    """
    if not _es_administrador(request):
        messages.error(request, 'Acceso restringido: Se requieren permisos de administrador para eliminar productos.')
        return redirect('lista')

    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        nombre = producto.nombre
        carrito = request.session.get('carrito', {})
        if str(id) in carrito:
            carrito.pop(str(id), None)
            request.session['carrito'] = carrito
            request.session.modified = True
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado exitosamente del catálogo.')
        return redirect('lista')

    contexto = {
        'producto': producto,
        'contenido': cargar_contenido(),
    }
    return render(request, 'catalogo/eliminar_producto.html', contexto)


def reporte_resumen(request):
    """
    Vista del Reporte 1 (Agrupación):
    Restringida exclusivamente a administradores.
    Agrupa los productos por categoría utilizando annotate de Django para calcular
    la cantidad de registros (Count), el promedio de precios (Avg) y la suma total de stock (Sum).
    Adicionalmente, utiliza aggregate para computar métricas consolidadas globales de todo el inventario.
    """
    if not _es_administrador(request):
        messages.error(request, 'Acceso restringido: Los reportes son de uso exclusivo para administradores.')
        return redirect('lista')

    categorias_reporte = Categoria.objects.annotate(
        total_productos=Count('productos'),
        promedio_precio=Avg('productos__precio'),
        stock_total=Sum('productos__stock'),
        precio_minimo=Min('productos__precio'),
        precio_maximo=Max('productos__precio'),
    ).order_by('nombre')

    metricas_globales = Producto.objects.aggregate(
        gran_total_productos=Count('id'),
        gran_total_stock=Sum('stock'),
        promedio_precio_global=Avg('precio'),
        precio_mas_alto=Max('precio'),
        precio_mas_bajo=Min('precio'),
    )

    contexto = {
        'categorias_reporte': categorias_reporte,
        'metricas_globales': metricas_globales,
        'titulo_reporte': 'Reporte de Productos por Categoría',
        'subtitulo_reporte': 'Agrupación estadística con cálculo de existencias y valores promedio por familia técnica.',
        'contenido': cargar_contenido(),
    }
    return render(request, 'catalogo/reporte_resumen.html', contexto)


def reporte_critico(request):
    """
    Vista del Reporte 2 (Filtrado):
    Restringida exclusivamente a administradores.
    Genera un listado de productos que cumplen una condición crítica de inventario
    (stock bajo o agotado). Aplica obligatoriamente los métodos filter y order_by del ORM
    para filtrar los productos por el umbral de stock y ordenarlos prioritariamente por
    stock ascendente y nombre.
    """
    if not _es_administrador(request):
        messages.error(request, 'Acceso restringido: El reporte de stock crítico es de uso exclusivo para administradores.')
        return redirect('lista')

    try:
        umbral = int(request.GET.get('umbral', 5))
        if umbral < 0:
            umbral = 5
    except (TypeError, ValueError):
        umbral = 5

    # Aplicación obligatoria de filter y order_by del ORM
    productos_criticos = (
        Producto.objects.filter(stock__lte=umbral)
        .select_related('categoria')
        .order_by('stock', 'nombre')
    )

    total_criticos = productos_criticos.count()
    total_agotados = sum(1 for p in productos_criticos if p.stock == 0)

    contexto = {
        'productos_criticos': productos_criticos,
        'umbral': umbral,
        'total_criticos': total_criticos,
        'total_agotados': total_agotados,
        'titulo_reporte': 'Reporte de Stock Crítico y Reposición',
        'subtitulo_reporte': f'Listado prioritario de artículos con inventario igual o inferior a {umbral} unidades.',
        'contenido': cargar_contenido(),
    }
    return render(request, 'catalogo/reporte_critico.html', contexto)


def contacto(request):
    """
    Vista para canalizar consultas y cotizaciones de clientes.
    Procesa ConsultaClienteForm vía POST, guarda en la base de datos y
    administra el contador de visitas a la sección mediante request.session.
    """
    # Funcionalidad de request.session: contador de visitas a la vista de contacto
    visitas = request.session.get('contador_visitas_contacto', 0) + 1
    request.session['contador_visitas_contacto'] = visitas
    request.session.modified = True

    # Recuperar los últimos productos visualizados guardados en sesión
    ultimos_vistos_ids = request.session.get('ultimos_vistos', [])
    ultimos_vistos = Producto.objects.filter(pk__in=ultimos_vistos_ids, visible=True)

    if request.method == 'POST':
        form = ConsultaClienteForm(request.POST)
        if form.is_valid():
            consulta = form.save()
            messages.success(
                request,
                f'¡Gracias por contactarnos, {consulta.nombre}! Tu consulta ha sido enviada exitosamente. '
                'Un asesor técnico de Ferretería Caro-Kahn responderá a tu correo a la brevedad.',
            )
            return redirect('contacto')
        else:
            messages.error(request, 'Por favor corrige los errores señalados a continuación en el formulario.')
    else:
        # Preseleccionar producto de interés si viene en el parámetro ?producto=ID
        initial_data = {}
        producto_id = request.GET.get('producto')
        if producto_id:
            try:
                initial_data['producto_interes'] = int(producto_id)
            except (ValueError, TypeError):
                pass
        form = ConsultaClienteForm(initial=initial_data)

    contexto = {
        'form': form,
        'visitas': visitas,
        'ultimos_vistos': ultimos_vistos,
        'titulo_pagina': 'Contacto y Asesoría Técnica',
        'subtitulo_pagina': 'Envíanos tus consultas técnicas, solicitudes de cotización o requerimientos de materiales.',
        'contenido': cargar_contenido(),
    }
    return render(request, 'catalogo/contacto.html', contexto)


def admin_consultas(request):
    """Bandeja de consultas técnicas de clientes, solo para administradores."""
    if not _es_administrador(request):
        messages.error(request, 'Debes iniciar sesión con una cuenta administradora.')
        return redirect(f"{reverse('login')}?next={reverse('admin_consultas')}")

    estado = request.GET.get('estado', 'pendientes')
    consultas = ConsultaCliente.objects.select_related('producto_interes', 'respondida_por')
    total_pendientes = consultas.filter(respondida_en__isnull=True).count()
    total_respondidas = consultas.filter(respondida_en__isnull=False).count()
    if estado == 'respondidas':
        consultas = consultas.filter(respondida_en__isnull=False)
    elif estado == 'todas':
        pass
    else:
        estado = 'pendientes'
        consultas = consultas.filter(respondida_en__isnull=True)

    contexto = {
        'consultas': consultas,
        'estado': estado,
        'total_pendientes': total_pendientes,
        'total_respondidas': total_respondidas,
        'total_todas': total_pendientes + total_respondidas,
        'contenido': cargar_contenido(),
    }
    return render(request, 'catalogo/admin_consultas.html', contexto)


def responder_consulta(request, id):
    """Permite al administrador responder una consulta; guarda y envía la respuesta por correo."""
    if not _es_administrador(request):
        messages.error(request, 'Debes iniciar sesión con una cuenta administradora.')
        return redirect(f"{reverse('login')}?next={reverse('admin_consultas')}")

    consulta = get_object_or_404(ConsultaCliente.objects.select_related('producto_interes'), pk=id)

    if request.method == 'POST':
        form = RespuestaConsultaForm(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['respuesta'].strip()
            consulta.respuesta = texto
            consulta.respondida_en = timezone.now()
            consulta.respondida_por = request.user
            consulta.save(update_fields=['respuesta', 'respondida_en', 'respondida_por'])
            RegistroAdministrativo.registrar(
                usuario=request.user,
                accion=RegistroAdministrativo.Accion.ACTUALIZACION,
                modelo="ConsultaCliente",
                objeto_id=consulta.pk,
                resumen=f"Se respondió la consulta de {consulta.nombre} ({consulta.correo}).",
            )
            marca = cargar_contenido().get('marca', 'Ferretería Caro-Kahn')
            cuerpo = (
                f"Hola {consulta.nombre},\n\n{texto}\n\n"
                f"--- Tu consulta original ---\n{consulta.mensaje}\n\n"
                f"Saludos cordiales,\nEquipo técnico de {marca}"
            )
            try:
                send_mail(
                    subject=f"Respuesta a tu consulta técnica — {marca}",
                    message=cuerpo,
                    from_email=None,
                    recipient_list=[consulta.correo],
                )
                messages.success(request, f'Respuesta enviada a {consulta.correo}.')
            except Exception:
                messages.warning(
                    request,
                    'La respuesta quedó guardada, pero no se pudo enviar el correo. '
                    'Revisa la configuración de correo o contacta al cliente manualmente.',
                )
            return redirect('admin_consultas')
        messages.error(request, 'Escribe una respuesta de al menos 10 caracteres.')
    else:
        form = RespuestaConsultaForm()

    contexto = {
        'consulta': consulta,
        'form': form,
        'contenido': cargar_contenido(),
    }
    return render(request, 'catalogo/responder_consulta.html', contexto)
