"""
A Python package for Partial Wave Analysis.

This is the python interface to `ComPWA
<https://github.com/ComPWA/ComPWA>`_, the “Common Partial Wave Analysis
framework”. In addition, this module provides some general tools that are
useful when doing PWA research with Python.
"""


__all__ = ['plotting', 'expertsystem', 'ui']

from . import plotting
from . import expertsystem
from . import ui
