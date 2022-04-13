# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# The critical thing is to make the path to the folder above 'alpaca' so that 
# Sphinx will see the alpaca folder as a package (due to the __init__.py in it).
#
import os
import sys
sys.path.insert(0, os.path.abspath('..\\..'))
sys.setrecursionlimit(1500)                         # Prevent Python crash on infinite recursion


# -- Project information -----------------------------------------------------

project = 'Alpyca - Python Client Library'
copyright = '2022, ASCOM Initiative, MIT License'
author = 'Bob Denny'

# The full version, including alpha/beta/rc tags
release = '0.1 alpha'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# RBD Added autodoc (https://www.sphinx-doc.org/en/master/usage/quickstart.html)
# and Napoleon https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
# for Alpyca Client project Python and Extended Google docstrings Also added 
# enum-tools[sphinx] to support :: autoenum: in the .rst files.
#
extensions = [
        'sphinx.ext.autodoc', 
        'sphinx.ext.autosummary',
        'sphinx.ext.napoleon',
        'enum_tools.autoenum'   #https://enum-tools.readthedocs.io/en/latest/api/autoenum.html
]

# Autodoc settings (override defaults)
autoclass_content = 'both'          # Concatenate class and __init__ 
autodoc_member_order = 'groupwise'  # Methods then Properties
autodoc_typehints = 'signature'
autodoc_typehints_format = 'short'
autodoc_default_options = {
    'show-inheritance': True
}

# Napoleon specific settings (most are the defaults)
# These for 'cloud' theme, makes notes and examples 
# far less overwhelming
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True        # Notes in shaded block :-)
napoleon_use_admonition_for_references = True
# napoleon_use_ivar = False
# napoleon_use_param = True
# napoleon_use_rtype = True
napoleon_preprocess_types = True
# napoleon_type_aliases = None
# napoleon_attr_annotations = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'cloud'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']