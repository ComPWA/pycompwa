"""A Python package for Partial Wave Analysis.

This is the python interface to `ComPWA <https://github.com/ComPWA/ComPWA>`__,
the “Common Partial Wave Analysis framework”. In addition, this module provides
some general tools that are useful when doing PWA research with Python.
"""


__all__ = [
    "data",
    "expertsystem",
    "plotting",
    "ui",
]


from . import data, expertsystem, plotting, ui
