"""CadQuery Electronics documentation."""

import os
import sys
from datetime import date

import sphinx_rtd_theme  # type: ignore[import-untyped] # noqa: F401

cq_electronics_path = os.path.dirname(os.path.abspath(os.getcwd()))
source_files_path = os.path.join(cq_electronics_path, "src/cq_electronics")
sys.path.insert(0, source_files_path)


project = "CadQuery Electronics"
release = "0.1.0"
author = "Seth Fischer"
project_copyright = f"{date.today().year}, {author}"


extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinxcontrib.cadquery",
]
templates_path = ["_templates"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

autodoc_mock_imports = [
    "cadquery",
]
