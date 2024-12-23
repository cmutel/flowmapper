"""Sphinx configuration."""

import importlib.metadata
import os
import shutil

from sphinx.ext import apidoc

# Run sphinx-apidoc
# This hack is necessary since RTD does not issue `sphinx-apidoc` before running
# `sphinx-build -b html . _build/html`. See Issue:
# https://github.com/readthedocs/readthedocs.org/issues/1139


__location__ = os.path.dirname(__file__)

output_dir = os.path.join(__location__, "api")
module_dir = os.path.join(__location__, "../flowmapper")
try:
    shutil.rmtree(output_dir)
except FileNotFoundError:
    pass

try:
    args = f"--implicit-namespaces -f -o {output_dir} {module_dir}".split(" ")
    apidoc.main(args)
except Exception as e:
    print("Running `sphinx-apidoc` failed!\n{}".format(e))

# General Configuration

project = "flowmapper"
author = "Francisco Alves de Oliveira Júnior"
copyright = "2023, Francisco Alves de Oliveira Júnior"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
autodoc_typehints = "description"
html_theme = "furo"

needs_sphinx = "7.2.6"

version = importlib.metadata.version("flowmapper")
