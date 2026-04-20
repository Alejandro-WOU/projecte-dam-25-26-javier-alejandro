Instalación y configuración del entorno
========================================

.. contents::
   :depth: 2
   :local:

Requisitos previos
------------------

Para desplegar el sistema Renaix necesitas:

- **Docker** y **Docker Compose** instalados en el sistema.
- **Python 3.10+** (para Sphinx y scripts de gestión).
- **Git** para clonar el repositorio.
- Puerto **8069** libre (Odoo) y **5432** (PostgreSQL).

Despliegue con Docker
---------------------

.. code-block:: bash

   # 1. Clona el repositorio
   git clone https://github.com/H3rr41z/Proyecto-Intermodular-DAM-2025.git
   cd projecte-dam-25-26-javier-alejandro

   # 2. Accede al directorio Docker
   cd erp/docker

   # 3. Levanta los contenedores
   docker-compose up -d

   # 4. Espera a que Odoo esté listo (~30-60 segundos)
   # Verifica con:
   docker logs -f odoo_container

   # 5. Accede a Odoo en http://localhost:8069

Primera configuración
---------------------

1. Accede a ``http://localhost:8069``.
2. Si es la primera vez, crea una base de datos:

   - **Nombre BD**: ``renaix_db`` (o el que prefieras).
   - **Email**: ``admin@renaix.com``
   - **Contraseña**: elige una contraseña segura.
   - Marca **"Cargar datos demo"** si quieres los datos de ejemplo.

3. Ve a **Ajustes → Activar modo desarrollador** (opcional para debugging).
4. Instala el módulo **Renaix** desde **Ajustes → Módulos**.

Variables de entorno
---------------------

El archivo ``docker-compose.yml`` acepta estas variables de entorno:

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Variable
     - Descripción
     - Valor por defecto
   * - ``POSTGRES_DB``
     - Nombre de la base de datos
     - ``odoo``
   * - ``POSTGRES_USER``
     - Usuario de PostgreSQL
     - ``odoo``
   * - ``POSTGRES_PASSWORD``
     - Contraseña de PostgreSQL
     - ``odoo``
   * - ``JWT_SECRET_KEY``
     - Clave secreta para firmar JWT
     - Ver ``config/settings.py``
   * - ``JWT_ACCESS_EXPIRY_HOURS``
     - Horas de validez del access token
     - ``24``
   * - ``JWT_REFRESH_EXPIRY_DAYS``
     - Días de validez del refresh token
     - ``30``

Generar esta documentación
--------------------------

.. code-block:: bash

   # Instalar dependencias de Sphinx
   pip install sphinx sphinx-rtd-theme myst-parser sphinx-autodoc-typehints

   # Desde la raíz del proyecto
   cd docs/sphinx

   # Generar HTML
   make html        # Linux/Mac
   make.bat html    # Windows

   # Ver resultado en:
   # docs/sphinx/_build/html/index.html

   # Regenerar API docs (opcional)
   sphinx-apidoc -o source/api ../../erp/docker/custom_addons --force
   make html
