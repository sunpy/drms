"""
Configuration file for the Sphinx documentation builder.
"""
import os
import datetime
from pathlib import Path

from sphinx_gallery.sorting import ExampleTitleSortKey
from sunpy_sphinx_theme.conf import *  # NOQA: F403

from drms import __version__

# -- Project information -----------------------------------------------------
project = "drms"
author = "The SunPy Project"
copyright = f"{datetime.datetime.now().year}, {author}"  # NOQA: A001

# The full version, including alpha/beta/rc tags
release = __version__
is_development = ".dev" in __version__

# -- General configuration ---------------------------------------------------
extensions = [
    "hoverxref.extension",
    "sphinx_copybutton",
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "sphinx_changelog",
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
]

# Set automodapi to generate files inside the generated directory
automodapi_toctreedirnm = "generated/api"
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

# -- Options for hoverxref -----------------------------------------------------
if os.environ.get("READTHEDOCS"):
    # Building on Read the Docs
    hoverxref_api_host = "https://readthedocs.org"
    if os.environ.get("PROXIED_API_ENDPOINT"):
        # Use the proxied API endpoint
        # - A RTD thing to avoid a CSRF block when docs are using a
        #   custom domain
        hoverxref_api_host = "/_"
hoverxref_tooltip_maxwidth = 600  # RTD main window is 696px
hoverxref_auto_ref = True
hoverxref_mathjax = True
# hoverxref has to be applied to these
hoverxref_domains = ["py"]
hoverxref_role_types = {
    # roles with py domain
    "attr": "tooltip",
    "class": "tooltip",
    "const": "tooltip",
    "data": "tooltip",
    "exc": "tooltip",
    "func": "tooltip",
    "meth": "tooltip",
    "mod": "tooltip",
    "obj": "tooltip",
    # roles with std domain
    "confval": "tooltip",
    "hoverxref": "tooltip",
    "ref": "tooltip",
    "term": "tooltip",
}

# -- Options for sphinx-copybutton ---------------------------------------------
# Python Repl + continuation, Bash, ipython and qtconsole + continuation, jupyter-console + continuation
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# -- Options for intersphinx extension ---------------------------------------
intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3/",
        (None, "http://www.astropy.org/astropy-data/intersphinx/python3.inv"),
    ),
    "numpy": (
        "https://numpy.org/doc/stable/",
        (None, "http://www.astropy.org/astropy-data/intersphinx/numpy.inv"),
    ),
    "scipy": (
        "https://docs.scipy.org/doc/scipy/reference/",
        (None, "http://www.astropy.org/astropy-data/intersphinx/scipy.inv"),
    ),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "astropy": ("https://docs.astropy.org/en/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "sunpy": ("https://docs.sunpy.org/en/stable/", None),
}

# -- Options for HTML output -------------------------------------------------
# Render inheritance diagrams in SVG
graphviz_output_format = "svg"
sphinx_gallery_conf = {
    "backreferences_dir": Path("generated") / "modules",
    "filename_pattern": "^((?!skip_).)*$",
    "examples_dirs": Path("..") / "examples",
    "within_subsection_order": ExampleTitleSortKey,
    "gallery_dirs": Path("generated") / "gallery",
    "default_thumb_file": Path(html_static_path[0]) / "img" / "sunpy_icon_128x128.png",  # NOQA: F405
    "abort_on_example_error": False,
    "plot_gallery": "True",
    "remove_config_comments": True,
    "doc_module": ("sunpy"),
    "only_warn_on_example_error": True,
    "matplotlib_animations": True,
}
