"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import shutil
import subprocess
import sys

# -- Project information -----------------------------------------------------
project = "pycompwa"
package = "pycompwa"
repo_name = "pycompwa"
copyright = "2020, ComPWA"  # noqa: A001
author = "Common Partial Wave Analysis"

# -- Generate API ------------------------------------------------------------
sys.path.insert(0, os.path.abspath("."))
from abbreviate_signature import abbreviate_signature  # noqa: E402

abbreviate_signature()
subprocess.call(
    " ".join(
        [
            # remove old API directory
            "rm -f $(ls api/*.rst | grep -v api/pycompwa.ui.rst) &&",
            # generate API
            "sphinx-apidoc",
            "--force",
            "--no-toc",
            "--templatedir _templates",
            "--separate",
            "-o api/",
            "../src/pycompwa/",
            # exclusions
            "../src/pycompwa/expertsystem/solvers/constraint",
            "../src/pycompwa/ui.*.so;",
            # overwrite pycompwa main module
            "cp api/pycompwa.inc api/pycompwa.rst",
        ]
    ),
    shell=True,
)


# -- General configuration ---------------------------------------------------
master_doc = "index.md"
source_suffix = {
    ".ipynb": "myst-nb",
    ".md": "myst-nb",
    ".rst": "restructuredtext",
}

# The master toctree document.
master_doc = "index"
modindex_common_prefix = [
    f"{package}.",
]

extensions = [
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_panels",
    "sphinx_thebe",
    "sphinx_togglebutton",
]
exclude_patterns = [
    "**.ipynb_checkpoints",
    "*build",
    "tests",
]

# General sphinx settings
add_module_names = False
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": ", ".join(
        [
            "__eq__",
        ]
    ),
}
html_copy_source = True  # needed for download notebook button
html_css_files = []
html_favicon = "_static/favicon.ico"
html_logo = "../src/ComPWA/doc/images/logo-small.png"
html_show_copyright = False
html_show_sourcelink = False
html_show_sphinx = False
html_sourcelink_suffix = ""
html_static_path = ["_static"]
html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": f"https://github.com/ComPWA/{repo_name}",
    "repository_branch": "stable",
    "path_to_docs": "docs",
    "use_download_button": True,
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "colab_url": "https://colab.research.google.com",
        "notebook_interface": "jupyterlab",
        "thebe": True,
        "thebelab": True,
    },
    "theme_dev_mode": True,
}
html_title = "pycompwa"
panels_add_bootstrap_css = False  # wider page width with sphinx-panels
pygments_style = "sphinx"
todo_include_todos = False
viewcode_follow_imported_members = True

# Cross-referencing configuration
default_role = "py:obj"
primary_domain = "py"
nitpicky = True  # warn if cross-references are missing
nitpick_ignore = [
    ("py:class", "ComPWA::Optimizer::Minuit2::MinuitResult"),
    ("py:class", "function"),
    ("py:class", "pandas.core.frame.DataFrame"),
    ("py:class", "pybind11_builtins.pybind11_object"),
    ("py:class", "pycompwa.expertsystem.solvers.constraint.Constraint"),
    ("py:class", "pycompwa.expertsystem.state.propagation.GraphElementTypes"),
]

# Settings for intersphinx
intersphinx_mapping = {
    "matplotlib": ("https://matplotlib.org/", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "python": ("https://docs.python.org/3", None),
    "pybind11": ("https://pybind11.readthedocs.io/en/stable", None),
}

# Settings for autosectionlabel
autosectionlabel_prefix_document = True

# Settings for copybutton
copybutton_prompt_is_regexp = True
copybutton_prompt_text = r">>> |\.\.\. "  # doctest

# Settings for linkcheck
linkcheck_anchors = False
linkcheck_ignore = [
    f"https://www.gemfony.eu/",
]

# Settings for myst_nb
execution_timeout = -1
nb_output_stderr = "remove"
nb_render_priority = {
    "html": (
        "application/vnd.jupyter.widget-view+json",
        "application/javascript",
        "text/html",
        "image/svg+xml",
        "image/png",
        "image/jpeg",
        "text/markdown",
        "text/latex",
        "text/plain",
    )
}
nb_render_priority["doctest"] = nb_render_priority["html"]

jupyter_execute_notebooks = "off"
if "EXECUTE_NB" in os.environ:
    print("\033[93;1mWill run Jupyter notebooks!\033[0m")
    jupyter_execute_notebooks = "force"

# Settings for myst-parser
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "dollarmath",
    "smartquotes",
]
myst_update_mathjax = False

# Settings for Thebe cell output
thebe_config = {
    "repository_url": html_theme_options["repository_url"],
    "repository_branch": html_theme_options["repository_branch"],
}
