# Configuration file for the Sphinx documentation builder.

project = "Biologger Sim"
copyright = "2025, Long Horizon Observatory"
author = "Daniel Fry"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = []

html_theme = "alabaster"
html_static_path: list[str] = ["_static"]
