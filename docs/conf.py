"""CadQuery Electronics documentation."""

from datetime import date

import sphinx_rtd_theme  # noqa: F401

project = "CadQuery Electronics"
release = "0.1.0"
author = "Seth Fischer"
copyright = f"{date.today().year}, {author}"


exclude_patterns = []
extensions = [
    "sphinx_rtd_theme",
]
templates_path = ["_templates"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
