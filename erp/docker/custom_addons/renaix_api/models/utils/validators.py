# -*- coding: utf-8 -*-
"""
Validadores reutilizables para datos de la API
"""

from ...config import settings


def validate_required_fields(data, required_fields):
    """
    Valida que todos los campos requeridos estén presentes.
    
    Args:
        data (dict): Datos a validar
        required_fields (list): Lista de campos requeridos
    
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not data:
        return False, 'No se proporcionaron datos'
    
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            missing_fields.append(field)
    
    if missing_fields:
        return False, f'Campos requeridos faltantes: {", ".join(missing_fields)}'
    
    return True, ''


def validate_price(precio):
    """
    Valida que un precio sea válido.
    
    Args:
        precio: Precio a validar
    
    Returns:
        bool: True si es válido
    """
    try:
        precio_float = float(precio)
        return 0 <= precio_float <= 1000000
    except (ValueError, TypeError):
        return False


def validate_pagination_params(page, limit):
    """
    Valida parámetros de paginación.
    
    Args:
        page: Número de página
        limit: Elementos por página
    
    Returns:
        tuple: (page_int, limit_int) validados
    """
    try:
        page_int = int(page) if page else 1
        limit_int = int(limit) if limit else settings.DEFAULT_PAGE_SIZE
    except (ValueError, TypeError):
        page_int = 1
        limit_int = settings.DEFAULT_PAGE_SIZE
    
    # Validar rangos
    page_int = max(1, page_int)
    limit_int = min(max(1, limit_int), settings.MAX_PAGE_SIZE)
    
    return page_int, limit_int


def validate_producto_data(data):
    """
    Valida datos de creación de producto.
    
    Args:
        data (dict): Datos del producto
    
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    # Campos requeridos
    required = ['nombre', 'precio', 'categoria_id']
    is_valid, error_msg = validate_required_fields(data, required)
    
    if not is_valid:
        return False, error_msg
    
    # Validar precio
    if not validate_price(data['precio']):
        return False, 'Precio inválido. Debe estar entre 0 y 1.000.000'
    
    # Validar nombre
    if len(data['nombre']) < 3:
        return False, 'El nombre debe tener al menos 3 caracteres'
    
    if len(data['nombre']) > 200:
        return False, 'El nombre no puede superar 200 caracteres'
    
    # Validar etiquetas (máximo 5)
    if data.get('etiqueta_ids') and len(data['etiqueta_ids']) > 5:
        return False, 'Un producto no puede tener más de 5 etiquetas'
    
    return True, ''


def validate_comentario_data(data):
    """
    Valida datos de comentario.
    
    Args:
        data (dict): Datos del comentario
    
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not data.get('texto'):
        return False, 'El comentario no puede estar vacío'
    
    texto = data['texto'].strip()
    
    if len(texto) < 3:
        return False, 'El comentario debe tener al menos 3 caracteres'
    
    if len(texto) > settings.MAX_COMMENT_LENGTH:
        return False, f'El comentario no puede superar {settings.MAX_COMMENT_LENGTH} caracteres'
    
    return True, ''


def validate_valoracion_data(data):
    """
    Valida datos de valoración.
    
    Args:
        data (dict): Datos de la valoración
    
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if 'puntuacion' not in data:
        return False, 'La puntuación es requerida'
    
    try:
        puntuacion = int(data['puntuacion'])
    except (ValueError, TypeError):
        return False, 'La puntuación debe ser un número'
    
    if puntuacion < 1 or puntuacion > 5:
        return False, 'La puntuación debe estar entre 1 y 5'
    
    # Validar comentario opcional
    if data.get('comentario'):
        if len(data['comentario']) > 500:
            return False, 'El comentario no puede superar 500 caracteres'
    
    return True, ''


def validate_mensaje_data(data):
    """
    Valida datos de mensaje.
    
    Args:
        data (dict): Datos del mensaje
    
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    required = ['receptor_id', 'texto']
    is_valid, error_msg = validate_required_fields(data, required)
    
    if not is_valid:
        return False, error_msg
    
    texto = data['texto'].strip()
    
    if len(texto) < 1:
        return False, 'El mensaje no puede estar vacío'
    
    if len(texto) > settings.MAX_MESSAGE_LENGTH:
        return False, f'El mensaje no puede superar {settings.MAX_MESSAGE_LENGTH} caracteres'
    
    return True, ''


def validate_denuncia_data(data):
    """
    Valida datos de denuncia.
    
    Args:
        data (dict): Datos de la denuncia
    
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    required = ['tipo', 'motivo', 'categoria']
    is_valid, error_msg = validate_required_fields(data, required)
    
    if not is_valid:
        return False, error_msg
    
    # Validar tipo
    valid_tipos = ['producto', 'comentario', 'usuario']
    if data['tipo'] not in valid_tipos:
        return False, f'Tipo inválido. Debe ser uno de: {", ".join(valid_tipos)}'
    
    # Validar que existe la referencia según el tipo
    if data['tipo'] == 'producto' and not data.get('producto_id'):
        return False, 'Debe especificar el producto a denunciar'
    
    if data['tipo'] == 'comentario' and not data.get('comentario_id'):
        return False, 'Debe especificar el comentario a denunciar'
    
    if data['tipo'] == 'usuario' and not data.get('usuario_reportado_id'):
        return False, 'Debe especificar el usuario a denunciar'
    
    # Validar motivo
    if len(data['motivo']) < 10:
        return False, 'El motivo debe tener al menos 10 caracteres'
    
    return True, ''


def validate_search_filters(filters):
    """
    Valida filtros de búsqueda de productos.
    
    Args:
        filters (dict): Filtros a validar
    
    Returns:
        dict: Filtros validados y limpios
    """
    validated = {}
    
    # Query de texto
    if filters.get('query'):
        validated['query'] = filters['query'].strip()
    
    # Categoría
    if filters.get('categoria_id'):
        try:
            validated['categoria_id'] = int(filters['categoria_id'])
        except (ValueError, TypeError):
            pass
    
    # Etiquetas (puede ser string separado por comas)
    if filters.get('etiquetas'):
        if isinstance(filters['etiquetas'], str):
            validated['etiquetas'] = [e.strip() for e in filters['etiquetas'].split(',') if e.strip()]
        elif isinstance(filters['etiquetas'], list):
            validated['etiquetas'] = filters['etiquetas']
    
    # Rango de precio
    if filters.get('precio_min'):
        try:
            validated['precio_min'] = float(filters['precio_min'])
        except (ValueError, TypeError):
            pass
    
    if filters.get('precio_max'):
        try:
            validated['precio_max'] = float(filters['precio_max'])
        except (ValueError, TypeError):
            pass
    
    # Estado del producto
    if filters.get('estado_producto'):
        validated['estado_producto'] = filters['estado_producto']
    
    # Ubicación
    if filters.get('ubicacion'):
        validated['ubicacion'] = filters['ubicacion'].strip()
    
    # Orden
    valid_orders = ['precio_asc', 'precio_desc', 'fecha_desc', 'fecha_asc']
    if filters.get('orden') and filters['orden'] in valid_orders:
        validated['orden'] = filters['orden']
    else:
        validated['orden'] = 'fecha_desc'  # Por defecto
    
    return validated
