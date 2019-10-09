.. image:: https://travis-ci.com/ComPWA/pycompwa.svg?branch=master
    :target: https://travis-ci.com/ComPWA/pycompwa
.. image:: https://zenodo.org/badge/212384131.svg
   :target: https://zenodo.org/badge/latestdoi/212384131
.. image:: https://badge.fury.io/py/pycompwa.svg
    :target: https://badge.fury.io/py/pycompwa
.. image:: https://readthedocs.org/projects/pycompwa/badge/?version=latest
    :target: https://pycompwa.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

About pycompwa
==============

pycompwa is a collection of python modules and the python interface to
`ComPWA <https://github.com/ComPWA/ComPWA>`_. ComPWA stands for 
"Common Partial Wave Analysis framework".

Analogous to ComPWA, pycompwas highest focus is also modularity. pycompwa
extends the ComPWA framework with some useful modules:

* `expertsystem <https://pycompwa.readthedocs.io/en/latest/python-modules.html#the-compwa-expert-system>`_
  
  A python package that can generate amplitude/intensity model files from simple
  user boundary conditions, such as inital and final state. Currently supports
  the helicity and canonical formalism.

* `plotting <https://pycompwa.readthedocs.io/en/latest/python-modules.html#plotting>`_

  Facilitates the visualization of data and results, i.e. comparison plots, Dalitz plots.

* `ui <https://pycompwa.readthedocs.io/en/latest/python-modules.html#python-ui>`_

  The python interface to ComPWA, allowing easy steering of ComPWA.

Installation
============

Detailed instructions can be found 
`here <https://pycompwa.readthedocs.io/en/latest/installation.html>`_.
Make sure the virtual environment is setup and activated.

Installation via pypi
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

   pip install pycompwa

Installation from source
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

   git clone --recurse-submodules git@github.com:ComPWA/pycompwa.git
   cd pycompwa
   python setup.py install -j4

Usage
=====

On how to use ComPWA please refer to the 
`Quickstart Example <https://github.com/ComPWA/pycompwa/blob/master/examples/jupyter/Quickstart.ipynb>`_.

Documentation
=============

The documentation can be found `here <https://pycompwa.readthedocs.io/en/latest>`_.