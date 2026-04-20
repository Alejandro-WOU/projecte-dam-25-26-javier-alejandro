# Proyecto-Intermodular-2025-26
Autores: Javier Herraiz Calatayud & Alejandro Sánchez Serrano

## Descripción general

Este repositorio recoge todo el trabajo realizado en el proyecto de compraventa de productos de segunda mano, desarrollado por nuestro equipo durante el curso 2025-26. El proyecto consta de dos aplicaciones principales:
- **ERP (Odoo, Docker, PostgreSQL):** plataforma para gestión y supervisión por parte de los empleados.
- **App móvil (Kotlin):** aplicación destinada a los usuarios para publicar, buscar y comprar productos.

El objetivo es facilitar la integración entre ambos sistemas y ofrecer una experiencia optimizada tanto al usuario final como al empleado administrador.

---

## Estructura del repositorio

```text
projecte-dam-25-26-javier-alejandro/
├── erp/                          # Código y configuración del ERP (Odoo + Docker)
│   ├── docker/
│   │   ├── custom_addons/
│   │   │   ├── renaix/           # Módulo core Odoo
│   │   │   └── renaix_api/       # Módulo API REST
│   │   └── docker-compose.yml
│   └── postman/                  # Colección Postman de la API
├── app-movil/                    # App Android (Kotlin + Jetpack Compose)
│   └── Renaix_APP/
├── docs/                         # Toda la documentación del proyecto (Fase 4)
│   ├── manuales/
│   │   ├── manual_odoo_empleados.md   # Manual de usuario Odoo web
│   │   └── manual_android.md          # Manual de usuario App Android
│   └── sphinx/                        # Documentación técnica automática (Sphinx)
│       ├── conf.py
│       ├── index.rst
│       ├── Makefile
│       ├── make.bat
│       ├── source/
│       │   ├── modules/
│       │   │   ├── renaix.rst         # Doc módulo core
│       │   │   └── renaix_api.rst     # Doc módulo API
│       │   ├── api/                   # Referencia autodoc
│       │   ├── instalacion.rst
│       │   └── seguridad.rst
│       └── _build/html/               # HTML generado (ejecutar: make html)
├── documentacion/                # Documentación general del proyecto
│   ├── Planificacion/
│   ├── Modulo Core/
│   └── API/
├── README.md
└── .gitignore
```

---

## Contenidos esenciales

- **erp/**  
  Todo lo necesario para desplegar el ERP, incluyendo el entorno dockerizado y los módulos personalizados.

- **app-movil/**  
  Código y recursos para la app móvil en Kotlin, además de manuales de instalación y los diagramas técnicos.

- **documentación-general/**  
  Documentos clave del proyecto, como requisitos funcionales y no funcionales, análisis y diseño de la base de datos, diagrama entidad-relación, arquitectura general del sistema (endpoints API REST), diagramas de clases y casos de uso.

---

## Organización del trabajo

Las tareas se han planificado y distribuido usando Trello.  
Cada componente del proyecto ha sido desarrollado por los integrantes según sus áreas de especialización:
- **ERP:** configuración, despliegue y administración de Odoo y la base de datos.
- **App móvil:** desarrollo en Kotlin y diseño de la experiencia de usuario.
- **Documentación:** creación y actualización constante de los documentos técnicos y diagramas.

Colaboramos mediante ramas de desarrollo y revisiones frecuentes en GitHub para asegurar la coherencia del trabajo.

---

## Documentación (Fase 4)

### Manuales de usuario

| Manual | Ruta | Descripción |
|--------|------|-------------|
| Manual Odoo (Empleados) | [docs/manuales/manual_odoo_empleados.md](docs/manuales/manual_odoo_empleados.md) | Guía de uso de la aplicación web Odoo para empleados |
| Manual App Android | [docs/manuales/manual_android.md](docs/manuales/manual_android.md) | Guía de uso de la app móvil Android para usuarios finales |

### Documentación técnica automática (Sphinx)

La documentación técnica de los módulos Odoo se genera con **Sphinx**.

**Generar el HTML:**

```bash
pip install sphinx sphinx-rtd-theme myst-parser sphinx-autodoc-typehints
cd docs/sphinx
make html        # Linux/Mac
make.bat html    # Windows
```

El resultado se genera en `docs/sphinx/_build/html/index.html`.

| Archivo fuente | Descripción |
|----------------|-------------|
| [docs/sphinx/source/modules/renaix.rst](docs/sphinx/source/modules/renaix.rst) | Módulo core: modelos, vistas, seguridad, informes |
| [docs/sphinx/source/modules/renaix_api.rst](docs/sphinx/source/modules/renaix_api.rst) | Módulo API REST: endpoints, autenticación JWT, ejemplos |
| [docs/sphinx/source/instalacion.rst](docs/sphinx/source/instalacion.rst) | Guía de instalación con Docker |
| [docs/sphinx/source/seguridad.rst](docs/sphinx/source/seguridad.rst) | Roles, permisos y seguridad JWT |

---

## Cómo navegar el repositorio

- Para la **documentación de usuario y técnica** (Fase 4), ve a [`docs/`](docs/).
- Para revisar el ERP, visita [`erp/docker/custom_addons/`](erp/docker/custom_addons/).
- Para la app móvil, examina [`app-movil/Renaix_APP/`](app-movil/Renaix_APP/).
- Para documentación general del proyecto (diagramas, planificación), ve a [`documentacion/`](documentacion/).

---

## Contribuyentes

- Alejandro-WOU
- H3rr41z

---

## Contacto

Para cualquier consulta técnica o sugerencia, utilizar los issues o contactar vía correo del repositorio.

---

