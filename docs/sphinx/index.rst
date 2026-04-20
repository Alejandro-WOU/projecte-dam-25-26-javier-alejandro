Renaix — Documentación Técnica de Módulos Odoo
===============================================

.. image:: https://img.shields.io/badge/version-1.0.0-blue
   :alt: Version 1.0.0

.. image:: https://img.shields.io/badge/odoo-16.0-purple
   :alt: Odoo 16.0

.. image:: https://img.shields.io/badge/python-3.10+-green
   :alt: Python 3.10+

**Proyecto:** Renaix — Marketplace de Segunda Mano

**Autores:** Javier Herraiz Calatayud & Alejandro Sánchez Serrano

**Curso:** 2º DAM 2025-2026 — IES Eduardo Primo Marqués

**Versión:** 1.0.0

---

Descripción general
-------------------

Renaix es una plataforma de compraventa de productos de segunda mano entre particulares.
El sistema consta de dos componentes principales desarrollados como módulos Odoo:

- **renaix**: Módulo core con toda la lógica de negocio, modelos de datos, vistas y dashboard.
- **renaix_api**: Módulo API REST con autenticación JWT para servir datos a la app móvil Android.

La app móvil Android (desarrollada en Kotlin + Jetpack Compose) consume la API del módulo
``renaix_api`` para ofrecer la experiencia de usuario final.

Arquitectura del sistema
------------------------

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │                   Renaix Platform                       │
   │                                                         │
   │  ┌──────────────┐    ┌─────────────────┐               │
   │  │  Odoo ERP    │    │  API REST        │               │
   │  │  (renaix)    │    │  (renaix_api)    │               │
   │  │              │    │                 │               │
   │  │ Dashboard    │    │  /api/v1/...    │               │
   │  │ Moderación   │    │  JWT Auth       │               │
   │  │ Estadísticas │    │  CRUD           │               │
   │  └──────────────┘    └────────┬────────┘               │
   │         │                     │                         │
   │  ┌──────┴─────────────────────┴────────┐               │
   │  │         PostgreSQL Database          │               │
   │  └──────────────────────────────────────┘               │
   └─────────────────────────────────────────────────────────┘
                                │
                     ┌──────────┴──────────┐
                     │   App Móvil Android  │
                     │   (Kotlin + Compose) │
                     └─────────────────────┘

Cómo generar esta documentación
---------------------------------

**Instalar dependencias:**

.. code-block:: bash

   pip install sphinx sphinx-rtd-theme myst-parser sphinx-autodoc-typehints

**Generar documentación HTML:**

.. code-block:: bash

   # Desde la raíz del proyecto
   cd docs/sphinx
   make html

   # En Windows
   make.bat html

**Ver el resultado:**

Abre ``docs/sphinx/_build/html/index.html`` en tu navegador.

**Regenerar API desde código fuente (opcional):**

.. code-block:: bash

   sphinx-apidoc -o source/api ../../erp/docker/custom_addons --force
   make html

---

Índice de contenidos
--------------------

.. toctree::
   :maxdepth: 3
   :caption: Módulos Odoo

   source/modules/renaix
   source/modules/renaix_api

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   source/api/renaix_models
   source/api/renaix_api_controllers

.. toctree::
   :maxdepth: 1
   :caption: Información adicional

   source/instalacion
   source/seguridad

---

Índice de búsqueda
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
