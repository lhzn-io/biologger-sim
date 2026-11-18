# Configuration file for the Sphinx documentation builder.

import inspect
import subprocess
import sys
from pathlib import Path
from typing import Any

# Document the checkout these docs live in, not whatever copy of the package is installed.
SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

project = "Biologger Sim"
copyright = "2025, Long Horizon Observatory"
author = "Long Horizon Observatory"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.linkcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.extlinks",
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

# Source links go to GitHub at the commit the docs were built from, so a line number in the
# docs always matches the code it describes. Outside git they fall back to main.
GITHUB = "https://github.com/lhzn-io/biologger-sim"


def _git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "main"


COMMIT = _git_commit()

# :src:`core/currents.py` links a file under src/biologger_sim/ at the build commit.
extlinks = {"src": (f"{GITHUB}/blob/{COMMIT}/src/biologger_sim/%s", "%s")}


def linkcode_resolve(domain: str, info: dict[str, str]) -> str | None:
    """GitHub URL, with line range, of a documented Python object at the build commit."""
    if domain != "py" or not info.get("module"):
        return None
    obj: Any = sys.modules.get(info["module"])
    if obj is None:
        return None
    for part in info["fullname"].split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError:
            return None
    if isinstance(obj, property):
        obj = obj.fget
    try:
        obj = inspect.unwrap(obj)
        source_file = inspect.getsourcefile(obj)
        lines, start = inspect.getsourcelines(obj)
    except (OSError, TypeError, ValueError):
        return None
    if source_file is None:
        return None
    try:
        rel = Path(source_file).resolve().relative_to(SRC.parent)
    except ValueError:
        return None  # defined outside this repository
    return f"{GITHUB}/blob/{COMMIT}/{rel.as_posix()}#L{start}-L{start + len(lines) - 1}"
