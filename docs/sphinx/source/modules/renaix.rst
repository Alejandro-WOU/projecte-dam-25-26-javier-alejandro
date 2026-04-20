Módulo: renaix (Core)
=====================

.. contents:: Tabla de contenidos
   :depth: 3
   :local:

Descripción funcional
---------------------

El módulo ``renaix`` es el núcleo de la plataforma Marketplace de Segunda Mano.
Implementa toda la lógica de negocio, los modelos de datos, las vistas para el
panel de empleados y las herramientas de moderación.

**¿Qué resuelve?**

- Gestión completa del ciclo de vida de productos de segunda mano.
- Sistema de usuarios de la app móvil integrado con ``res.partner`` de Odoo.
- Control y moderación de comentarios, denuncias e incidencias.
- Dashboard con estadísticas y gráficos para empleados.
- Informes PDF imprimibles (reportes QWeb).
- Sistema de permisos con 4 niveles de acceso.

Instalación y dependencias
---------------------------

Dependencias de Odoo
~~~~~~~~~~~~~~~~~~~~

El módulo depende de los siguientes módulos nativos de Odoo:

.. code-block:: python

   'depends': [
       'base',      # Modelos base de Odoo
       'mail',      # Chatter y notificaciones
       'contacts',  # res.partner
   ]

Instalación en Docker
~~~~~~~~~~~~~~~~~~~~~

El módulo se despliega automáticamente con el entorno Docker del proyecto:

.. code-block:: bash

   # Desde erp/docker/
   docker-compose up -d

   # Acceder a Odoo en:
   # http://localhost:8069

   # Instalar el módulo desde la interfaz:
   # Ajustes → Módulos → Renaix

O mediante CLI:

.. code-block:: bash

   docker exec -it odoo_container odoo -d renaix_db -i renaix --stop-after-init

Estructura de archivos
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   renaix/
   ├── __init__.py
   ├── __manifest__.py
   ├── models/
   │   ├── categoria.py
   │   ├── comentario.py
   │   ├── compra.py
   │   ├── denuncia.py
   │   ├── etiqueta.py
   │   ├── mensaje.py
   │   ├── producto.py
   │   ├── producto_imagen.py
   │   ├── res_company.py
   │   └── res_partner.py
   ├── views/
   │   ├── menu.xml
   │   ├── producto_views.xml
   │   ├── denuncia_views.xml
   │   ├── estadisticas_views.xml
   │   └── ...
   ├── security/
   │   ├── security.xml
   │   └── ir.model.access.csv
   ├── data/
   │   └── *.xml  (datos demo)
   └── reports/
       └── report_partner_activity.xml

Modelos principales
-------------------

Producto (renaix.producto)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Modelo central de la plataforma. Representa los artículos de segunda mano publicados por usuarios.

.. code-block:: python

   class Producto(models.Model):
       _name = 'renaix.producto'
       _description = 'Producto de Segunda Mano'
       _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

**Campos relevantes:**

.. list-table::
   :header-rows: 1
   :widths: 20 15 50 15

   * - Campo
     - Tipo
     - Descripción
     - Obligatorio
   * - ``name``
     - Char
     - Nombre descriptivo del producto
     - Sí
   * - ``descripcion``
     - Text
     - Descripción detallada
     - No
   * - ``precio``
     - Float
     - Precio en euros
     - Sí
   * - ``estado_producto``
     - Selection
     - Condición física: nuevo, como_nuevo, buen_estado, aceptable, para_reparar
     - Sí
   * - ``estado_venta``
     - Selection
     - Ciclo de vida: borrador, disponible, reservado, vendido, eliminado
     - Sí
   * - ``propietario_id``
     - Many2one → res.partner
     - Usuario propietario del producto
     - Sí
   * - ``categoria_id``
     - Many2one → renaix.categoria
     - Categoría del producto
     - No
   * - ``etiqueta_ids``
     - Many2many → renaix.etiqueta
     - Etiquetas/hashtags (máx. 5)
     - No
   * - ``imagen_ids``
     - One2many → renaix.producto.imagen
     - Imágenes del producto
     - No
   * - ``ubicacion``
     - Char
     - Ciudad o código postal
     - No
   * - ``antiguedad``
     - Char
     - Tiempo de uso (ej: "6 meses")
     - No
   * - ``fecha_publicacion``
     - Datetime
     - Fecha de publicación (auto)
     - Sí

**Reglas de negocio:**

- Un producto solo puede tener un máximo de 5 etiquetas.
- El estado cambia de borrador → disponible → reservado → vendido.
- Al marcar como "eliminado" el producto se oculta sin borrar del sistema.
- Hereda de ``image.mixin`` para gestión nativa de imágenes en Odoo.

Etiqueta (renaix.etiqueta)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clasificador de productos mediante hashtags normalizados.

.. code-block:: python

   class Etiqueta(models.Model):
       _name = 'renaix.etiqueta'
       _description = 'Etiqueta de Producto'

**Campos relevantes:**

.. list-table::
   :header-rows: 1
   :widths: 20 15 50

   * - Campo
     - Tipo
     - Descripción
   * - ``name``
     - Char
     - Nombre normalizado (lowercase, sin espacios dobles)
   * - ``color``
     - Integer
     - Color de visualización en chips/kanban
   * - ``active``
     - Boolean
     - Si False, no aparece como opción
   * - ``producto_count``
     - Integer (computed)
     - Número de productos con esta etiqueta

**Reglas de validación:**

- Mínimo 2 caracteres, máximo 30.
- Único en base de datos (case-insensitive).
- Se normaliza automáticamente a minúsculas al crear/editar.
- Restricción SQL: ``UNIQUE(LOWER(name))``.

Denuncia (renaix.denuncia)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sistema de moderación de contenido inapropiado.

.. code-block:: python

   class Denuncia(models.Model):
       _name = 'renaix.denuncia'
       _description = 'Denuncia'
       _inherit = ['mail.thread', 'mail.activity.mixin']

**Campos relevantes:**

.. list-table::
   :header-rows: 1
   :widths: 20 15 50 15

   * - Campo
     - Tipo
     - Descripción
     - Obligatorio
   * - ``tipo``
     - Selection
     - Qué se denuncia: producto, comentario, usuario
     - Sí
   * - ``producto_id``
     - Many2one → renaix.producto
     - Producto denunciado (si tipo=producto)
     - Condicional
   * - ``comentario_id``
     - Many2one → renaix.comentario
     - Comentario denunciado (si tipo=comentario)
     - Condicional
   * - ``usuario_reportado_id``
     - Many2one → res.partner
     - Usuario denunciado (si tipo=usuario)
     - Condicional
   * - ``usuario_reportante_id``
     - Many2one → res.partner
     - Quién hace la denuncia
     - Sí
   * - ``motivo``
     - Text
     - Descripción del motivo (mín. 10 chars)
     - Sí
   * - ``categoria``
     - Selection
     - Tipo: spam, fraude, violencia, contenido_inapropiado, informacion_falsa, otro
     - Sí
   * - ``estado``
     - Selection
     - pendiente, en_revision, resuelta, rechazada
     - Sí
   * - ``empleado_asignado_id``
     - Many2one → res.users
     - Moderador responsable
     - No
   * - ``resolucion``
     - Text
     - Acción tomada
     - No

**Flujo de estados:**

.. code-block:: text

   pendiente → en_revision → resuelta
                           → rechazada

**Comportamiento al crear:**

- Notifica automáticamente a todos los moderadores del sistema.
- Crea una actividad pendiente para el primer moderador del grupo.

Usuario App (res.partner extendido)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extensión del modelo nativo ``res.partner`` de Odoo para usuarios de la app móvil.

**Campos añadidos:**

.. list-table::
   :header-rows: 1
   :widths: 25 15 50

   * - Campo
     - Tipo
     - Descripción
   * - ``es_usuario_app``
     - Boolean
     - Identifica usuarios de la app (vs contactos normales)
   * - ``partner_gid``
     - Char
     - UUID global para sincronización con app móvil
   * - ``fecha_registro_app``
     - Datetime
     - Fecha de registro en la app
   * - ``valoracion_promedio``
     - Float (computed)
     - Media de valoraciones recibidas como vendedor (0-5)
   * - ``productos_en_venta``
     - Integer (computed)
     - Productos disponibles actualmente
   * - ``productos_vendidos``
     - Integer (computed)
     - Total de productos vendidos
   * - ``cuenta_activa``
     - Boolean
     - Si False, el usuario no puede autenticarse en la app

Comentario (renaix.comentario)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comentarios públicos de usuarios en productos.

**Campos relevantes:**

.. list-table::
   :header-rows: 1
   :widths: 20 15 50

   * - Campo
     - Tipo
     - Descripción
   * - ``producto_id``
     - Many2one → renaix.producto
     - Producto comentado
   * - ``usuario_id``
     - Many2one → res.partner
     - Autor del comentario
   * - ``texto``
     - Text
     - Contenido del comentario
   * - ``fecha``
     - Datetime
     - Fecha de publicación (auto)
   * - ``active``
     - Boolean
     - False si fue eliminado por moderación

Compra (renaix.compra)
~~~~~~~~~~~~~~~~~~~~~~~

Transacciones de compraventa entre usuarios.

**Campos relevantes:**

.. list-table::
   :header-rows: 1
   :widths: 20 15 50

   * - Campo
     - Tipo
     - Descripción
   * - ``producto_id``
     - Many2one → renaix.producto
     - Producto transaccionado
   * - ``comprador_id``
     - Many2one → res.partner
     - Usuario comprador
   * - ``vendedor_id``
     - Many2one → res.partner
     - Usuario vendedor
   * - ``precio_final``
     - Float
     - Precio acordado en la transacción
   * - ``estado``
     - Selection
     - pendiente, completada, cancelada
   * - ``fecha_compra``
     - Datetime
     - Fecha de la transacción

Seguridad y roles
-----------------

El módulo define 4 grupos de acceso:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Grupo
     - ID Técnico
     - Permisos
   * - **Usuario**
     - ``renaix.group_renaix_user``
     - Solo lectura en todos los modelos
   * - **Moderador**
     - ``renaix.group_renaix_moderador``
     - Lectura + escritura + creación en la mayoría; puede gestionar denuncias y comentarios
   * - **Administrador**
     - ``renaix.group_renaix_admin``
     - Acceso completo (CRUD) en todos los modelos
   * - **Manager**
     - ``renaix.group_renaix_manager``
     - Acceso administrativo completo + configuración del sistema

**Resumen de accesos (ir.model.access.csv):**

.. code-block:: text

   Modelo              | Usuario | Moderador | Admin
   --------------------|---------|-----------|-------
   renaix.producto     |  R      |  RWCD     |  RWCD
   renaix.etiqueta     |  R      |  RWC      |  RWCD
   renaix.denuncia     |  RC     |  RWCD     |  RWCD
   renaix.comentario   |  R      |  RWCD     |  RWCD
   renaix.compra       |  R      |  RWC      |  RWCD
   renaix.valoracion   |  R      |  RWCD     |  RWCD

   R=Read, W=Write, C=Create, D=Delete

Vistas y menús
--------------

El módulo registra las siguientes vistas principales:

**Menú principal Renaix:**

.. code-block:: text

   Renaix
   ├── Productos
   │   ├── Todos los Productos      (list, form, kanban, search)
   │   └── Imágenes de Productos   (list, form)
   ├── Usuarios
   │   └── Usuarios App            (list, form, search)
   ├── Transacciones
   │   ├── Compras                 (list, form)
   │   └── Valoraciones            (list, form)
   ├── Comunicación
   │   ├── Comentarios             (list, form)
   │   └── Mensajes                (list, form)
   ├── Moderación
   │   └── Denuncias               (list, form, search)
   ├── Estadísticas
   │   ├── Resumen General         (graph, pivot)
   │   └── Dashboard               (dashboard)
   └── Configuración
       ├── Categorías              (list, form)
       └── Etiquetas               (list, form)

**Tipos de vistas por modelo:**

- **Producto**: list, form, kanban, search, graph, pivot
- **Denuncia**: list, form, search (con filtros rápidos: pendiente, en_revisión)
- **Estadísticas**: 4 gráficos (barras, líneas, circular, pivot)

Informes (Reports)
------------------

El módulo incluye un informe QWeb en PDF:

- **report_partner_activity**: Informe de actividad de usuarios (productos publicados, compras, valoraciones).

Generación:

.. code-block:: python

   # Desde código Python/Odoo shell
   env['ir.actions.report'].search([('report_name', '=', 'renaix.report_partner_activity')]).render_qweb_pdf([partner_id])

Referencia de API (autodoc)
----------------------------

.. automodule:: renaix.models.producto
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: renaix.models.etiqueta
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: renaix.models.denuncia
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: renaix.models.res_partner
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: renaix.models.comentario
   :members:
   :undoc-members:
   :show-inheritance:
