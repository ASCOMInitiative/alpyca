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
sys.path.insert(0, os.path.abspath('..//..'))
# Prevent Python crash on infinite recursion
sys.setrecursionlimit(1500)


# -- Project information -----------------------------------------------------

project = 'Alpyca: API Library for Alpaca'
copyright = '2022-2024, ASCOM Initiative, MIT License'
author = 'Bob Denny'

# The full version, including alpha/beta/rc tags
release = '3.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
#
# RBD Added autodoc (https://www.sphinx-doc.org/en/master/usage/quickstart.html)
# and Napoleon https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
# for Alpyca project Python and Extended Google docstrings Also added
# enum-tools[sphinx] to support :: autoenum: in the .rst files.
#
#                       =============
#                       == WARNING ==
#                       =============
#   Package importlib-metadata must be 4.11.4 or rinoh will fail
#   It's possible that any version less than 6.0.0 will work.
#
extensions = [
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
    'sphinx.ext.autodoc',
    # https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
    'sphinx.ext.autosummary',
    # https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
    'sphinx.ext.napoleon',
    # https://github.com/sphinx-contrib/restbuilder
    'sphinxcontrib.restbuilder',
    # https://enum-tools.readthedocs.io/en/latest/api/autoenum.html
    'enum_tools.autoenum',
    # https://github.com/brechtm/rinohtype  Makes PDF
    'rinoh.frontend.sphinx'
]

# Autodoc settings (override defaults)
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration
autoclass_content = 'both'          # Concatenate class and __init__
autodoc_class_signature = 'mixed'   # Display signature with class name!
# Required due to superclass, else mixes things up
autodoc_member_order = 'groupwise'
autodoc_typehints = 'signature'
autodoc_typehints_format = 'short'
autodoc_default_options = {
    'show-inheritance': True
}

# Napoleon specific settings
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True        # Notes in shaded block :-)
napoleon_use_admonition_for_references = True
napoleon_preprocess_types = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output --

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes and the link below for a more comprehensive list.
# The link below leads to the chosen style and all of its features are shown.
#
# https://sphinx-themes.org/sample-sites/sphinx-rtd-theme/
html_theme = 'sphinx_rtd_theme'

#
# Clean up ugly aspects of Read The Docs. See comments in the css
#
html_style = 'css/ascom.css'

# -- Options for PDF Output using rinohtype --

# Here are the settings per the rinohtype docs
#   https://www.mos6581.org/rinohtype/master/index.html#
# The docs for the available rinoh_documents options are at
#   https://www.mos6581.org/rinohtype/master/sphinx.html
# Invokes as > sphinx-build -b rinoh source build/PDF  (I have a makepdf.bat)

rinoh_documents = [dict(doc='index',                # top-level file (index.rst)
                        target='alpyca',            # output file (alpyca.pdf)
                        title='Alpyca Library',
                        subtitle='Release 3.0.0',
                        author='Robert B. Denny <rdenny@dc3.com>',
                        logo='alpaca1000.png',
                        template='alpyca.rtt')]
