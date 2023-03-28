# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

import os
from drms import __version__
from pathlib import Path
from sphinx_gallery.sorting import ExampleTitleSortKey
from sunpy_sphinx_theme.conf import *  # NOQA

project = "drms"
copyright = "2023, The SunPy Developers"
author = "The SunPy Developers"

# The full version, including alpha/beta/rc tags
release = __version__
is_development = ".dev" in __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "sphinx_gallery.gen_gallery",
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_changelog",
]
numpydoc_show_class_members = False

# Add any paths that contain templates here, relative to this directory.

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The reST default role (used for this markup: `text`) to use for all
# documents. Set to the "smart" one.
default_role = "obj"

# Enable nitpicky mode, which forces links to be non-broken
nitpicky = True
nitpick_ignore = [
    ("py:obj", "numpy.datetime64"),
    # See https://github.com/numpy/numpy/issues/10039
]

# -- Options for intersphinx extension -----------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "astropy": ("https://docs.astropy.org/en/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "sunpy": ("https://docs.sunpy.org/en/stable/", None),
}

# -- Options for HTML output -------------------------------------------------
os.environ["JSOC_EMAIL"] = "jsoc@sunpy.org"
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Nfontsize=10",
    "-Nfontname=Helvetica Neue, Helvetica, Arial, sans-serif",
    "-Efontsize=10",
    "-Efontname=Helvetica Neue, Helvetica, Arial, sans-serif",
    "-Gfontsize=10",
    "-Gfontname=Helvetica Neue, Helvetica, Arial, sans-serif",
]

# -- Sphinx Gallery ------------------------------------------------------------
sphinx_gallery_conf = {
    "backreferences_dir": Path("generated") / "modules",
    "filename_pattern": "^((?!skip_).)*$",
    "examples_dirs": Path("..") / "examples",
    "within_subsection_order": ExampleTitleSortKey,
    "gallery_dirs": Path("generated") / "gallery",
    # Comes from the theme.
    "default_thumb_file": Path(html_static_path[0]) / "img" / "sunpy_icon_128x128.png",
    "abort_on_example_error": False,
    "only_warn_on_example_error": True,
    "plot_gallery": True,
    "remove_config_comments": True,
    "doc_module": ("sunpy"),
}
