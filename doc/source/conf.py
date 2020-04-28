#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ComPWA documentation build configuration file, created by
# sphinx-quickstart on Thu Jan 18 12:52:15 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import shutil
import subprocess

# It is assumed that you run sphinx from the virtual environment which
# includes pycompwa

# -- Copy example notebooks ---------------------------------------------------
print("Copy example notebook files")
PATH_SOURCE = "../../examples"
PATH_TARGET = "usage"
EXAMPLE_FOLDERS_TO_COPY = [
    "tools",
    "workflow",
]
IGNORED_PATTERNS = shutil.ignore_patterns("*/.ipynb_checkpoints/*",)
for root, dirs, _ in os.walk(PATH_TARGET):
    for directory in dirs:
        path = os.path.join(root, directory)
        print("  remove directory", path)
        shutil.rmtree(path)
for root, dirs, _ in os.walk(PATH_SOURCE):
    for directory in dirs:
        if directory not in EXAMPLE_FOLDERS_TO_COPY:
            continue
        path_from = os.path.join(root, directory)
        path_to = os.path.join(PATH_TARGET, directory)
        print("  copy", path_from, "to", path_to)
        shutil.copytree(
            path_from, path_to, symlinks=True, ignore=IGNORED_PATTERNS,
        )
shutil.copyfile(
    os.path.join(PATH_SOURCE, "particle_list.xml"),
    os.path.join(PATH_TARGET, "particle_list.xml"),
    follow_symlinks=True,
)

# -- Generate API skeleton ----------------------------------------------------
subprocess.call(
    "rm -f $(ls api/*.rst | grep -v api/pycompwa.ui.rst) && "
    "sphinx-apidoc "
    "--force "
    "--no-toc "
    "--templatedir _templates "
    "--separate "
    "-o api/ ../../pycompwa/ "
    "../../pycompwa/expertsystem/solvers/constraint "
    "../../pycompwa/ui.*.so; "
    "cp api/pycompwa_overwrite api/pycompwa.rst",
    shell=True,
)


def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]

# Cross-referencing configuration
default_role = "py:obj"
primary_domain = "py"
nitpicky = True  # warn if cross-references are missing
nitpick_ignore = [
    ("py:class", "function"),
    ("py:class", "pycompwa.expertsystem.solvers.constraint.Constraint"),
    ("py:class", "pycompwa.expertsystem.state.propagation.GraphElementTypes"),
    ("py:class", "pybind11_builtins.pybind11_object"),
]

# Settings for intersphinx
intersphinx_mapping = {
    "matplotlib": ("https://matplotlib.org/", None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "python": ("https://docs.python.org/3", None),
    "pybind11": ("https://pybind11.readthedocs.io/en/stable", None),
}

# Settings for autosectionlabel
autosectionlabel_prefix_document = True

# Settings for linkcheck
linkcheck_anchors = False
linkcheck_ignore = [
    f"https://www.gemfony.eu/",
]

# Settings for nbsphinx
if "NBSPHINX_EXECUTE" in os.environ:
    nbsphinx_execute = "always"
else:
    nbsphinx_execute = "never"
nbsphinx_timeout = -1
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [
    ".rst",
    ".ipynb",
]

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "pycompwa"
copyright = "2019, ComPWA Team"
author = "Remco de Boer, Mathias Michel, Stefan Pflüger, Peter Weidenkaff"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogues.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    "**.ipynb_checkpoints",
    "_build",
    "build",
    "tests",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

add_module_names = False  # True is the default
modindex_common_prefix = ["pycompwa."]

viewcode_follow_imported_members = True

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": True,
    "display_version": True,
    "prev_next_buttons_location": "both",
    "style_external_links": False,
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": False,
    "titles_only": False,
}

html_logo = "../../ComPWA/doc/images/logo-small.png"

html_copy_source = False  # do not copy rst files

html_show_sourcelink = False
html_show_copyright = False
html_show_sphinx = False

html_context = {
    "display_github": True,
    "github_user": "ComPWA",
    "github_repo": "pycompwa",
    "github_version": "master/doc/source/",
}

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    "**": [
        "about.html",
        "navigation.html",
        "relations.html",  # needs 'show_related': True theme option to display
        "searchbox.html",
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "pycompwadoc"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "pycompwa.tex", "pycompwa Documentation", author, "manual"),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "pycompwa", "pycompwa Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "pycompwa",
        "pycompwa Documentation",
        author,
        "pycompwa",
        "",
        "Miscellaneous",
    ),
]
