Explica las instrucciones del archivo adjunto // Explica a detalle y dame los comandos necesarios para la "Etapa 0" //
Recomienda un "Prompt" para cumplir con las siguientes características: ...... Según el archivo.
 
Consulta 1:

"Actúa como un desarrollador backend generando datos de prueba. Necesito que crees un arreglo JSON válido con exactamente 40 objetos que representen el catálogo de una ferretería.
Cada objeto debe contener obligatoriamente los siguientes campos:  id: un número entero secuencial del 1 al 40.nombre: el nombre del producto (sé variado y realista).categoria: la clasificación del artículo (ej. Herramientas manuales, Fijaciones).precio: un número entero positivo en pesos chilenos.stock: un número entero entre 0 y 50. Es fundamental que al menos 5 productos tengan el stock en "0" para poder probar la lógica condicional visual de la interfaz.
Devuelve únicamente el arreglo JSON, sin explicaciones adicionales ni bloques de texto."

Respuesta de la IA: Entregó un arreglo JSON válido con 40 objetos estructurados con los campos solicitados y variaciones de stock, incluyendo valores en cero.

Qué se usó o modificó: Se utilizó el código generado tal cual para crear el archivo productos.json, aunque se revisaron manualmente los montos de los precios para asegurar que fueran realistas para el mercado chileno.

Consulta 2:

"Actúa como un desarrollador front end experto en Django. Necesito diseñar la interfaz para un catálogo web de una ferretería utilizando Django Template Language (DTL).

Requisitos técnicos y de diseño:
1. Genera dos archivos:
   - 'base.html': Plantilla base que incluya un encabezado con el nombre de la ferretería, barra de navegación simple, bloque {% block content %} y un pie de página. Usa Bootstrap 5 vía CDN para los estilos.
   - 'lista.html': Plantilla que herede de 'base.html'. Debe mostrar una cuadrícula responsiva (cards) que itere una lista de objetos 'productos' usando un bucle {% for producto in productos %}.
2. Cada tarjeta de producto debe mostrar:
   - Nombre del producto
   - Categoría
   - Precio formateado
   - Stock disponible
   - Un botón o enlace que apunte a la vista de detalle: {% url 'detalle' producto.id %}
3. Entrega el código HTML limpio, semántico y listo para copiar en la carpeta de templates."

Respuesta de la IA: Generó el código base con las etiquetas de herencia ({% extends %}, {% block content %}) y un bucle {% for %} básico, utilizando clases del framework Bootstrap 5.

Qué se usó o modificó: Se extrajo únicamente la lógica de sintaxis de Django (bucle condicionales y URLs). Se descartó por completo el código de Bootstrap propuesto, ya que se optó por construir un diseño propio con CSS puro.

Consulta 3:

"Actúa como un desarrollador Front End Senior. Necesito estructurar y añadir nuevas funcionalidades visuales a la Landing Page (plantillas base.html y lista.html) de un proyecto académico en Django. El sitio es un catálogo online para una ferretería enfocada en materiales técnicos e infraestructura.

Necesito que me generes el código HTML semántico y el CSS puro (sin frameworks como Bootstrap) considerando los siguientes requerimientos:

Nuevas Funciones en la Interfaz:

Diseña una 'Barra de Búsqueda' simulada en el encabezado (header).

Crea una barra lateral (aside) o sección superior de 'Filtros Rápidos' utilizando botones o etiquetas (ej. Herramientas Manuales, Diseño Estructural de Pavimentos, Insumos para Refuerzo de Taludes, Mezclas Asfálticas).

Añade un pie de página (footer) con enlaces de contacto y un diseño corporativo.

Estructura HTML y CSS:

Utiliza CSS Grid para organizar el listado de productos de forma fluida.

Utiliza Flexbox para el encabezado y la alineación de los filtros.

La paleta de colores debe ser profesional e industrial: tonos grises asfalto, blanco para lectura clara y un color de acento de alta visibilidad (como naranja o amarillo de seguridad).

Todo el CSS debe estar debidamente comentado y ordenado por secciones (Variables, Globales, Layout, Componentes).

Integración con Django:

El código debe respetar la sintaxis de herencia de templates ({% block content %}, {% extends %}).

Por favor, entrégame el código de base.html y lista.html por separado, y explica brevemente cómo esta estructura mejora la mantenibilidad del proyecto."

Respuesta de la IA: Proporcionó una estructura semántica y un bloque de estilos CSS puro organizado por variables, enfocándose en una paleta de colores industrial y un diseño responsivo utilizando CSS Grid.

Qué se usó o modificó: Se integró el código CSS en la etiqueta <style> de base.html. Se modificaron las variables de color hexadecimales (--acento, --asfalto) para ajustarlas a la identidad del catálogo y se adaptaron los nombres de las clases para que coincidieran con el HTML previo.

Consulta 4:

"Actúa como un desarrollador experto en Django y frontend. Estoy construyendo la Etapa 3 de un catálogo web de ferretería. La restricción técnica principal es que no puedo usar modelos ni conexión a base de datos; todos los productos se procesan desde un archivo productos.json leído en views.py.

Necesito que me entregues el código de las vistas (views.py) y los templates (HTML/JS) para simular las siguientes cuatro funcionalidades sin romper la restricción de la base de datos:

Imágenes: Modifica la estructura de mi JSON actual para incluir un campo imagen_url con enlaces a imágenes de placeholder gratuitas enfocadas en materiales de construcción, herramientas o infraestructura vial. Actualiza el template para renderizarlas.

Filtro Dinámico: Crea un script en JavaScript puro para lista.html que permita filtrar en tiempo real las tarjetas de productos por categoria y por rango de precio, ocultando los elementos del DOM dinámicamente sin recargar la página ni hacer consultas al backend.

Simulación de Compra: Diseña un botón de 'Añadir al carro' en la vista de detalle. Al hacer clic, utiliza la API de localStorage de JavaScript para guardar temporalmente los productos seleccionados y muestra un modal confirmando la reserva del pedido, simulando el proceso de forma estática.

Panel de Administración (Mockup): Crea una ruta, una vista y un template llamado admin_landing.html. Debe lucir como un panel de control con un formulario HTML que simule la edición del título de la página principal. Al enviar el formulario mediante POST, la vista debe simplemente retornar un mensaje de éxito usando el framework messages de Django, sin guardar nada en disco."

Respuesta de la IA: La herramienta generó un bloque de código extenso que incluía la actualización del archivo JSON con enlaces a imágenes de prueba, un script en JavaScript para filtrar tarjetas en el frontend, y toda la lógica (vistas, rutas y HTML) para simular un carrito de compras y un panel de control estático.  

Qué se usó o modificó: Se integró únicamente el campo de imágenes en el JSON y el script de JavaScript puro para el filtro dinámico, ya que representan una mejora visual válida para la Etapa 3 que opera exclusivamente en el lado del cliente. Se descartó y eliminó por completo todo el código relacionado con el carrito de compras, el inicio de sesión y el panel de administración, ya que estos elementos excedían los límites de las instrucciones de la evaluación y añadían rutas innecesarias que podían generar errores de ejecución.

Consulta 5:

Actúa como un desarrollador Front End Senior experto en Django Template Language y diseño web moderno.

Necesito rediseñar y reestructurar mi catálogo web de ferretería en Django (nombre: 'Ferretería Caro-Kahn') para transformarlo de un listado simple en una Landing Page moderna, persuasiva y estéticamente atractiva, completamente en español.

Requisitos de Estructura y Contenido (Landing Page):

Diseña una estructura persuasiva que incluya las siguientes secciones principales:

Sección Héroe (Hero Section): Un encabezado de pantalla completa con un título impactante (ej: "Materiales y Soluciones Profesionales para tus Proyectos de Construcción"), una descripción convincente y un botón de Llamado a la Acción (CTA) grande y visible (ej: "Explora Nuestro Catálogo Técnico").

Sección de Beneficios (Why Us): Tres o cuatro tarjetas minimalistas que expliquen las ventajas competitivas de la ferretería (ej: "Asesoría Técnica Experta", "Stock Garantizado", "Envío Directo a Obra", "Calidad Certificada").

Sección del Catálogo (Adaptada): Integra la cuadrícula de productos existente, pero con un diseño de tarjetas (cards) mucho más limpio y atractivo. Mantén el bucle {% for producto in productos %}, pero cada tarjeta debe tener una imagen grande (simulada con placehold.co), nombre, categoría, precio formateado y un botón de detalle elegante.

Sección de Testimonios (Mockup): Una sección estática simulando opiniones de clientes satisfechos (ingenieros, constructores) para generar confianza.

Sección de Llamado a la Acción Final: Un panel de cierre invitando a cotizar, contactar o descargar un catálogo técnico.

Estética Moderna y Detalles Visuales:

Utiliza CSS puro (sin frameworks como Bootstrap) para un diseño minimalista y ligero.

Aplica una cuadrícula responsiva (CSS Grid) para el catálogo y Flexbox para el layout general.

Elige una paleta de colores profesional e industrial, inspirada en las capturas previas: grises asfalto (`#252a2e`), blanco para claridad (`#ffffff`) y un color de acento de alta visibilidad como naranja o amarillo seguridad (`#f5a900`).

Utiliza una tipografía moderna sans-serif legible (como Segoe UI o similar).

Añade micro-interacciones sutiles, como efectos de `hover` suaves en las tarjetas y botones, y un diseño "aireado" con buen uso de espacios en blanco.

Integración con Django:

El código debe respetar la sintaxis de herencia de templates ({% block content %}, {% extends 'catalogo/base.html' %}).

Por favor, entrégame el código de `base.html` y `lista.html` (o `landing.html`, si prefieres renombrarlo) por separado, con todo el CSS incrustado en `<style>` en `base.html` y `<style scoped>` o similar en `lista.html` (o el CSS separado y explicado cómo integrarlo).

Explica brevemente cómo esta estructura mejora la mantenibilidad del proyecto.

Respuesta de la IA:
Entregó el código completo para base.html y lista.html, estructurando una Landing Page completa que incluía la Sección Héroe, tarjetas de beneficios, el catálogo con CSS Grid, testimonios y un llamado a la acción final, aplicando correctamente la paleta de colores asfalto/amarillo y la sintaxis de Django.

Qué se usó o modificó:
Se extrajo y utilizó el CSS puro para la cuadrícula responsiva (Grid) de las tarjetas de productos y la estructuración del encabezado. Sin embargo, se eliminaron por completo las secciones de "Héroe", "Beneficios", "Testimonios" y "Llamado a la Acción Final", ya que añadían contenido estático que excedía el alcance de las instrucciones de la evaluación. El código se redujo para mantener únicamente la visualización del catálogo y el resumen calculado, asegurando el cumplimiento estricto de la rúbrica.

Consulta 6:

"Actúa como un desarrollador backend experto en Django. Necesito implementar el sistema CRUD completo para el modelo principal de mi aplicación de ferretería ('Producto'), utilizando ModelForm y vistas basadas en funciones.

Requerimientos específicos:
1. Formulario (forms.py):
   - Crea una clase ProductoForm que herede de forms.ModelForm vinculada al modelo Producto.
   - Incluye los campos: nombre, categoria, precio, stock, imagen_url, descripcion y visible.
   - Aplica etiquetas legibles en español, widgets personalizados con clases CSS y validación para evitar precios o stocks negativos.
2. Vistas (views.py):
   - crear_producto: Instancia el formulario vacío (GET) o procesa los datos (POST). Si es válido, guarda y redirige con un mensaje de éxito a la vista del catálogo principal ('lista').
   - editar_producto: Recibe el ID del producto, obtiene la instancia existente con get_object_or_404, instancia el formulario vinculado a dicha entidad y, tras guardar exitosamente por POST, redirige a 'lista'.
   - eliminar_producto: Recibe el ID, muestra una plantilla de confirmación (GET) y, al confirmar mediante POST, elimina el objeto de la base de datos y redirige a 'lista'.
3. Mapeo de URLs (urls.py):
   - Conecta las rutas: path('agregar/', ...), path('editar/<int:id>/', ...) y path('eliminar/<int:id>/', ...).
4. Templates:
   - 'formulario_producto.html': Plantilla unificada que renderice el formulario usando {{ form.as_p }} tanto para creación como para edición, respetando la estética del sitio.
   - 'eliminar_producto.html': Plantilla de confirmación con método POST y token CSRF que pregunte al usuario antes de borrar el producto.
   - 'lista.html': Añade botones de 'Editar' y 'Eliminar' junto a cada producto del catálogo, además de un botón destacado para agregar nuevos registros."

Respuesta de la IA:
Proporcionó la estructura del formulario ProductoForm con validaciones personalizadas en clean_precio y clean_stock, las 3 vistas funcionales con redirección a 'lista', la configuración de rutas en urls.py y el código HTML para formulario_producto.html y eliminar_producto.html, sugiriendo además enlaces de acción en cada tarjeta de lista.html.

Qué se usó o modificó:
Se adoptó la arquitectura de ModelForm y las tres vistas funcionales con sus correspondientes redirecciones POST hacia 'lista'. Se adaptaron los widgets y las plantillas para integrarse coherentemente con los tokens de diseño (variables CSS, colores #20292D, #F9B313, #F4F5F2 y componentes tipo tarjeta) de Ferretería Caro-Kahn, incorporando también limpieza del producto en el carrito de sesión en caso de eliminación y estilos modulares en formulario.css sin romper ninguno de los tests preexistentes del proyecto.

Consulta 7:

"Actúa como un desarrollador backend senior experto en Django ORM. Necesito implementar dos vistas de reportes y analíticas para una ferretería:

1. Reporte 1 (Agrupación):
   - Una vista ('reporte_resumen') que agrupe los productos por categoría utilizando las funciones de agregación del ORM (annotate y aggregate).
   - Debe calcular para cada categoría la cantidad de productos asociados (Count), el promedio de precios (Avg) y la suma total de stock (Sum), además de precios mínimos y máximos.
   - Debe incluir métricas consolidadas globales mediante aggregate para totalizar productos, stock total y promedio global de la ferretería.
2. Reporte 2 (Filtrado):
   - Una vista ('reporte_critico') que filtre los productos que cumplan con una condición de inventario crítico (stock menor o igual a un umbral definido, por ejemplo 5 unidades).
   - Es obligatorio utilizar los métodos filter() y order_by() del ORM para obtener la información ordenada prioritariamente por menor stock y nombre del producto.
3. Configuración de rutas y plantillas:
   - Rutas en urls.py: path('reporte-resumen/', ...) y path('reporte-critico/', ...).
   - Plantillas HTML independientes ('reporte_resumen.html' y 'reporte_critico.html') que extiendan base.html y muestren los resultados finales en tablas iteradas con {% for %}, sin realizar cálculos en el template.
   - Enlaces directos a ambos reportes en la barra de navegación de base.html."

Respuesta de la IA:
Entregó la formulación de las consultas del ORM con Categoria.objects.annotate(total_productos=Count('productos'), promedio_precio=Avg('productos__precio'), stock_total=Sum('productos__stock')) y Producto.objects.aggregate(...), la consulta de filtrado Producto.objects.filter(stock__lte=umbral).order_by('stock', 'nombre'), las definiciones de rutas en urls.py y la estructura HTML semántica de las tablas con iteradores para ambos reportes.

Qué se usó o modificó:
Se implementaron íntegramente las consultas con annotate, aggregate, filter y order_by en views.py. Se enriqueció la experiencia visual creando una hoja de estilos modular (reportes.css) alineada a la paleta de colores institucional, se incorporó un selector dinámico de umbral de stock en el reporte crítico y se actualizaron los menús de navegación en base.html (tanto en el header como en el pie de página) para garantizar el acceso directo desde todo el sitio.

Consulta 8:

"Actúa como un desarrollador backend y frontend experto en Django. Necesito resolver tres requerimientos en el proyecto:

1. Modelo y Formulario de Contacto:
   - Crear el modelo 'ConsultaCliente' con campos obligatorios: nombre, correo y mensaje; producto_interes como ForeignKey opcional (blank=True, null=True) a Producto; y fecha con auto_now_add=True.
   - Registrar ConsultaCliente en admin.py con list_display y filtros.
   - Generar y aplicar las migraciones correspondientes.
   - Crear 'ConsultaClienteForm' como ModelForm con validaciones que verifiquen campos obligatorios, formato válido de correo y un largo mínimo para el mensaje.
   - Configurar la vista 'contacto' para procesar POST, guardar con form.save(), enviar mensajes de confirmación e implementar gestión de sesiones con request.session (contador de visitas y lista de últimos 3 productos visualizados).
   - Renderizar el template 'contacto.html' con token {% csrf_token %} y validación de errores.

2. Seguridad y Separación de Roles:
   - Restringir las operaciones administrativas (creación, edición y eliminación de productos) verificando que el usuario tenga rol de administrador/staff. Redirigir a usuarios casuales o clientes con mensaje de error si intentan acceder.
   - Ocultar los botones de administración ('+ Agregar nuevo producto', 'Editar' y 'Eliminar') en lista.html para usuarios no administradores.

3. Escalado y Responsividad de la Interfaz:
   - Corregir el desbordamiento horizontal en el encabezado (.navbar) y pie de página cuando la ventana se escala o hace zoom, aplicando flex-wrap, overflow-x: hidden y puntos de quiebre responsivos intermedios (1200px y 960px)."

Respuesta de la IA:
Proporcionó la definición de ConsultaCliente en models.py, su registro en admin.py, los comandos de migración, la clase ConsultaClienteForm en forms.py con métodos clean personalizados, la vista contacto en views.py con almacenamiento en request.session del contador de visitas y últimos 3 productos vistos en detalle, el template contacto.html con {% csrf_token %}, la lógica de control de acceso basada en request.user.is_staff en vistas y templates, y reglas de CSS para solventar el escalado responsivo en base.css.

Qué se usó o modificó:
Se implementaron íntegramente las validaciones y el almacenamiento del modelo en la base de datos tras ejecutar makemigrations y migrate. En cuanto a roles, se aplicó un filtro estricto con _es_administrador() en crear_producto, editar_producto y eliminar_producto para blindar el backend frente a usuarios no privilegiados, además de condicionar el renderizado en lista.html. Para el escalado, se ajustó el header con flex-wrap y se añadieron breakpoints a 1200px y 960px evitando barras de desplazamiento horizontal al redimensionar o aplicar zoom.

Consulta 9:

"Actúa como un desarrollador senior experto en UX/UI y arquitectura web en Django. Necesito refactorizar la barra de navegación del sitio para separar de forma tajante la experiencia del cliente y la del administrador, además de restringir por completo los módulos de Stock Crítico y Reportes al rol administrativo:

1. Separación de Contextos de Navegación:
   - Navegación Pública (Clientes): Solo debe mostrar enlaces orientados a clientes: Inicio, Catálogo, Categorías, Servicios y Contacto. En la zona derecha: Buscador estilizado, Cotización (con badge numérico discreto), e inicio de sesión / menú de usuario. Los módulos de Reportes y Stock Crítico NO deben ser visibles para usuarios casuales ni en el header ni en el footer.
   - Navegación Administrativa (Gestión): Cuando el usuario con permisos de staff se encuentra en el área de administración (admin_landing, reportes, stock crítico, etc.), el header debe cambiar a modo de gestión: mostrar el badge 'Administración', enlaces a Resumen, Productos, Stock Crítico, Reportes y Contenido; y en la derecha un botón 'Ver tienda' para regresar a la tienda pública, junto al menú de perfil del administrador.
2. Seguridad en Vistas:
   - Proteger reporte_resumen y reporte_critico en views.py para que rechacen peticiones de usuarios sin rol staff, redirigiendo al catálogo con mensaje de error.
3. Componentes y Estilos:
   - Crear un menú de perfil de usuario desplegable con <details class='user-menu'> y summary.
   - Consolidar la paleta con variables semánticas (--nav-background, --brand-yellow, etc.), línea inferior amarilla para elementos activos con [aria-current='page'], y buscador centrado y prominente."

Respuesta de la IA:
Propuso la arquitectura de doble navegación en base.html soportada por un context processor que evalúa el estado del usuario y la ruta actual, las reglas de bloqueo con _es_administrador() en views.py para reporte_resumen y reporte_critico, el componente de menú desplegable <details class='user-menu'>, y el bloque de estilos CSS estructurado con los tokens de diseño y los estados activos para [aria-current='page'].

Qué se usó o modificó:
Se actualizó catalogo/context_processors.py para inyectar es_admin y es_area_admin globalmente en todas las plantillas. Se refactorizó base.html y base.css para alternar automáticamente entre la barra pública y la administrativa. Se protegieron backend y frontend para ocultar y denegar de forma absoluta los reportes y el stock crítico a clientes y usuarios no autorizados, garantizando además que las 50 pruebas unitarias del proyecto pasen con un 100% de éxito.

Consulta 10:

"Actúa como un diseñador de interfaces y desarrollador Front End Senior en Django. Necesito aplicar mejoras visuales profundas y corregir detalles de interfaz en las vistas del administrador y la navegación global del sitio:

1. Corrección de Contraste y Navegación:
   - Corregir el distintivo 'Administración' (.header__badge-admin) en el encabezado administrativo para que tenga un alto contraste legible (fondo amarillo de seguridad #F9B313 con texto oscuro #20292D).
   - Eliminar definitivamente los enlaces de gestión administrativa ('Reportes' y 'Stock Crítico') de la barra de navegación pública del catálogo para evitar sobrecarga y desbordamiento visual; estos módulos solo deben ser accesibles cuando se está en el modo de gestión administrativa o a través del menú de perfil del administrador.
   - Corregir el menú desplegable del perfil (.user-menu__dropdown) para garantizar un fondo completamente sólido y oscuro (#20292D), bordes definidos, tipografía de alto contraste (#FFFFFF), efectos hover diferenciados (#2C373B) y alineación derecha que impida desbordamientos horizontales.

2. Mejoras Visuales en el Panel de Administración (admin_landing.html y admin.css):
   - Incorporar una grilla de tarjetas KPI ejecutivas en el dashboard administrativo para visualizar rápidamente el total de productos, alertas de stock crítico, quiebres de inventario (agotados) y módulos activos.
   - Expandir la navegación modular del panel administrativo mediante tarjetas responsivas con enlaces a gestión de inventario, formulario rápido, ModelForm completo, stock crítico, reportes por categoría y contenido del sitio.
   - Enriquecer la lista de productos administrativos con indicadores visuales de nivel de stock (badges para 'Agotado', 'Stock bajo' y 'Stock normal') y botones directos a la edición y eliminación con confirmación.

3. Mejoras en Vistas de Reportes y Analíticas (reportes.css):
   - Añadir acción de impresión oficial ('Imprimir reporte') con reglas CSS específicas para @media print que oculten encabezados y elementos interactivos para generar documentos limpios.
   - Aplicar rayado alternado (zebra striping) en las tablas de resultados para optimizar la legibilidad en pantallas grandes."

Respuesta de la IA:
Proporcionó la reestructuración de clases CSS para el badge administrativo y el menú desplegable, las definiciones de tokens semánticos en base.css y admin.css, la inclusión de las tarjetas KPI en el panel de control alimentadas desde views.py, los badges de stock condicionales y la configuración de estilos de impresión profesional para los reportes.

Qué se usó o modificó:
Se implementaron los estilos de alto contraste en el badge de administración y el menú de usuario en base.css, eliminando la fuga de enlaces administrativos hacia la barra pública. En admin_landing.html y admin.css se integraron las métricas ejecutivas clave y los badges de stock por producto, conectando además el panel con las vistas de ModelForm y confirmación de eliminación. En reportes.css se añadieron las reglas para impresión y filas alternadas, verificando con 50 pruebas automatizadas que el sistema conserve total integridad y rendimiento.

Conclusión:

Durante el desarrollo de esta primera evaluación en los laboratorios de INACAP Sede Osorno, utilicé la Inteligencia Artificial principalmente como una herramienta para acelerar la escritura de código repetitivo y maquetar el diseño front-end. Le pedí generar los 40 registros en formato JSON porque inventar cada material de ferretería a mano habría consumido demasiado tiempo de la prueba. Esa respuesta me sirvió tal cual, permitiéndome enfocarme en la lógica de views.py. Por otro lado, al solicitar el diseño de la interfaz, la IA tendía a sobre-complicar el código sugiriendo el uso de Bootstrap o inventando funcionalidades fuera de alcance, como sistemas de carrito de compras o paneles de administración. Tuve que corregir exhaustivamente esas respuestas, eliminando todo el código sobrante para no romper la restricción de la evaluación, que exige trabajar sin base de datos. En este proceso aprendí que es vital aplicar un filtro crítico a las respuestas de la IA, asegurándome de extraer únicamente la herencia de plantillas, el bucle de iteración y el CSS puro que necesitaba para cumplir estrictamente con la mejora visual.