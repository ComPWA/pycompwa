Installation
============

There are two possibilities to install pycompwa:

* install from pypi (releases only)
* build from source 

The detailed steps for these two installation possibilities are explained below.

.. tip::

   In either case, it is highly recommended to setup and use a python virtual
   environment for pycompwa. Use the tool of your liking, popular choices are 
   `pipenv <https://github.com/pypa/pipenv>`_ and 
   `venv <https://docs.python.org/3/tutorial/venv.html>`_.

Prerequisites
-------------

pycompwa is designed to run on most modern unix systems (including MacOS).
When installing pycompwa from pypi, no precompiled binaries are used, but
instead the source is downloaded and build. Therefore the following packages
are mandatory for both installation variants:

* scikit-build (python package)

  Install via ``pip install scikit-build``
* requirements of `ComPWA <https://github.com/ComPWA/ComPWA#prerequisites>`_:
  
  * cmake
  * gcc or clang
  * Boost
  * optional libraries: ROOT, Geneva, ...

.. note::
   
   Since pycompwa uses and builds ComPWA in the background, all requirements of
   ComPWA are inherited. 


Installation from pypi
----------------------

If you plan to only work with a release version, this variant is the easiest and most convenient.
Make sure your virtual environment is activated, then simply run

.. code-block:: shell

   pip install pycompwa

Installation from source
------------------------

Getting the source
^^^^^^^^^^^^^^^^^^

To get the most recent version of pycompwa, clone its GitHub repository:

.. code-block:: shell

   git clone --recurse-submodules git@github.com:ComPWA/pycompwa.git <PYCOMPWA_SOURCE_PATH>

this will clone the repository to the subfolder ``<PYCOMPWA_SOURCE_PATH>``
within the current directory. pycompwa includes several, submodules

Building & Installing
^^^^^^^^^^^^^^^^^^^^^

First navigate into the source directory of pycompwa

.. code-block:: shell

  cd <PYCOMPWA_SOURCE_PATH>

Make sure the virtual environment is setup and activated. Then the building and
installation of pycompwa is also simply:

.. code-block:: shell

   python setup.py install -j4
   
This will build ComPWA and all submodules via cmake and install all necessary
files into the python environment. Alternatively you can run ``pip install .``.
This does not build multithreaded though...

That's it. On how to use ComPWA please refer to the 
:ref:`Quickstart Example <example_quickstart>`.

.. tip::

   Of course pycompwa can also be used with `jupyter <https://jupyter.org/>`_.
   You can install jupyter into your virtual environment via ``pip install jupyter``
   Then just navigate to the jupyter examples subdirectory ``examples/jupyter``
   and run ``jupyter notebook``. 

Testing the pycompwa installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can run the test suite in the pycompwa source directory via

.. code-block:: shell
   
   cd tests
   python -m pytest


Updating pycompwa
-----------------

You can update to newer versions of pycompwa via

.. code-block:: shell

   pip install pycompwa --upgrade


We would be happy to recieve some feedback or contributions ;)!