import os
import sys

# Add the project root to sys.path so Sphinx can find modules
sys.path.insert(0, os.path.abspath(".."))

project = "Brookside BI"
author = "Brookside"
release = "1.0.0"
version = "1.0.0"

extensions = [
    "myst_parser",
]

# Enable parsing of both RST and Markdown files
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Paths for templates and static files
templates_path = ["_templates"]
html_static_path = ["_static"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
