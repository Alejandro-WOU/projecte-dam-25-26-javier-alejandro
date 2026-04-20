# -*- coding: utf-8 -*-
"""
Sphinx configuration — Renaix Odoo Modules Documentation
Proyecto Intermodular DAM 2025-2026
"""

import os
import sys

# -- Path setup ---------------------------------------------------------------
# Añadimos los módulos Odoo al path para que autodoc pueda importarlos.
# En un entorno real con Odoo instalado, se necesita configurar odoo en el sys.path.
# Para generar sin Odoo instalado, usamos mock de los imports.

sys.path.insert(0, os.path.abspath('../../erp/docker/custom_addons'))

# -- Project information -------------------------------------------------------

project = 'Renaix — Módulos Odoo'
copyright = '2026, Javier Herraiz Calatayud & Alejandro Sánchez Serrano'
author = 'Javier Herraiz Calatayud & Alejandro Sánchez Serrano'
release = '1.0.0'
version = '1.0'

# -- General configuration -----------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',       # Documentación automática desde docstrings
    'sphinx.ext.napoleon',      # Soporte para Google/NumPy style docstrings
    'sphinx.ext.viewcode',      # Enlace al código fuente
    'sphinx.ext.intersphinx',   # Links a documentación de otros proyectos
    'sphinx.ext.todo',          # Soporte para .. todo::
    'myst_parser',              # Soporte para Markdown (.md)
]

# Fuentes de documentación aceptadas
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Archivo principal del índice
master_doc = 'index'

# Idioma de la documentación
language = 'es'

# Directorios y archivos a excluir
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**/__pycache__']

# -- Autodoc configuration -----------------------------------------------------

# Mock de imports de Odoo para que autodoc pueda procesar sin Odoo instalado
autodoc_mock_imports = [
    'odoo',
    'odoo.models',
    'odoo.fields',
    'odoo.api',
    'odoo.http',
    'odoo.exceptions',
    'odoo.tools',
    'werkzeug',
    'psycopg2',
    'lxml',
    'PIL',
    'PyJWT',
    'jwt',
]

# Documentar miembros privados (comenzados con _) si se especifica explícitamente
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'show-inheritance': True,
}

# Añadir tipo de retorno en la firma del método
autodoc_typehints = 'description'

# -- Napoleon (Google/NumPy style) ----------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- Todo configuration --------------------------------------------------------
todo_include_todos = True

# -- HTML output ---------------------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
}

html_static_path = ['_static']
templates_path = ['_templates']

html_title = f'{project} v{release}'
html_short_title = 'Renaix — Documentación'

html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'

html_css_files = ['custom.css']

# -- Post-process viewcode pages to inject custom CSS --------------------------
# Las páginas _modules/ generadas por viewcode no reciben html_css_files,
# así que inyectamos el <link> manualmente tras el build.

def inject_css_in_modules(app, exception):
    """Inyecta custom.css en todas las páginas _modules/ generadas por viewcode."""
    if exception:
        return
    import os
    from pathlib import Path

    outdir = Path(app.outdir)
    modules_dir = outdir / '_modules'
    if not modules_dir.exists():
        return

    css_tag = '<link rel="stylesheet" type="text/css" href="{depth}_static/custom.css" />\n'

    for html_file in modules_dir.rglob('*.html'):
        content = html_file.read_text(encoding='utf-8')
        if 'custom.css' in content:
            continue  # ya tiene el link
        # Calcular profundidad relativa para la ruta correcta
        rel = html_file.relative_to(outdir)
        depth = '../' * (len(rel.parts) - 1)
        tag = css_tag.format(depth=depth)
        # Insertar justo antes del cierre </head>
        content = content.replace('</head>', tag + '</head>', 1)
        html_file.write_text(content, encoding='utf-8')


def setup(app):
    app.connect('build-finished', inject_css_in_modules)

# -- Intersphinx ---------------------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
