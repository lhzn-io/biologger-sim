# Configuration file for the Sphinx documentation builder.

project = "Biologger Sim"
copyright = "2025, Long Horizon Observatory"
author = "Long Horizon Observatory"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
]

templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = []

html_theme = "lhzn"
html_static_path: list[str] = ["_static"]
html_theme_options = {
    "source_repository": "https://github.com/lhzn-io/biologger-sim",
    "source_branch": "main",
    "source_directory": "docs/source/",
}
