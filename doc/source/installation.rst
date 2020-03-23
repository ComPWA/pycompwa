.. |br| raw:: html

  <br />

Installation
============

It is best to install the pycompwa framework within a virtual environment, so
that all dependencies of pycompwa are contained within there. We recommend to
use `Anaconda <https://www.anaconda.com/distribution/>`__ in combination with
`Conda-Forge <https://conda-forge.org/>`__.

After you have `installed Anaconda
<https://docs.anaconda.com/anaconda/install/>`__, set Conda-Forge as the
default channel as follows:

.. code-block:: shell

  conda config --add channels conda-forge
  conda config --set channel_priority strict

Now, create a new environment with `all required dependencies
<https://github.com/ComPWA/pycompwa/blob/master/requirements.txt>`__
installed:

.. code-block:: shell

  conda create -n compwa --file requirements.txt

Here, we call the environment ``compwa``, but you can give it any name. Now, go
into this environment with ``conda activate compwa``, so we can install
pycompwa there:

.. code-block:: shell

  pip install scikit-build
  pip install pycompwa

Note that ``scikit-build`` has to be installed first.

That's it! You can now go through the :ref:`Quickstart` to learn how to use
pycompwa.

.. tip::

    Of course, pycompwa can also be used with `jupyter
    <https://jupyter.org/>`__. You can install jupyter in your virtual Conda
    environment via ``conda install jupyter``. Then, just navigate to the
    jupyter examples  ``examples/jupyter`` and run ``jupyter notebook``.

Prerequisites
-------------

ComPWA and the pycompwa interface have the following dependencies:

* ``scikit-build`` (a python package) |br|
  Install via ``pip install scikit-build``
* requirements of `ComPWA <https://github.com/ComPWA/ComPWA#prerequisites>`__:

  * Build tool: `cmake <https://cmake.org/>`__
  * Compiler: ``gcc`` or ``clang``
  * `Boost <https://www.boost.org/>`__
  * optional libraries: |br|
    `ROOT <https://root.cern.ch/downloading-root>`__ and/or `Minuit
    <http://seal.web.cern.ch/seal/snapshot/work-packages/mathlibs/minuit/>`__,
    `Geneva <https://www.gemfony.eu/>`__, and
    `GSL <https://www.gnu.org/software/gsl/>`__

* The Python requirements listed `here
  <https://github.com/ComPWA/pycompwa/blob/master/requirements.txt>`__

Installation from source
------------------------

If you are a pycompwa developer, you will have to build the framework from
source instead of using the pycompwa release that is distributed through
``conda``. See :ref:`Developer Mode <DeveloperMode>` for the installation
instructions.
