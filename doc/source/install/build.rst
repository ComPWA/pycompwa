Build and install
=================

Once you :doc:`have the source code <get-the-source-code>` and have
:doc:`activated the virtual environment <virtual-environment>`, you're ready to
build and install `pycompwa`.

When you install `pycompwa`, you are telling the system where to find it. There
are two ways of doing this:

(1) by copying the source code and binaries to a folder known to the system
    (you do this :ref:`with setuptools <setuptools>`)
(2) by telling the system to directly monitor the :doc:`local repository
    <get-the-source-code>` as the installation path (we call this
    :ref:`'developer mode' <install/build:Developer Mode>`).

The second option is more dynamic, because any changes to the source code are
immediately available at runtime, which allows you to tweak the code and try
things out. When using the first option, you would have to run ``setuptools``
again to make the changes known to the system.


.. _setuptools:

Using ``setuptools``
~~~~~~~~~~~~~~~~~~~~

This is easy-peasy! Just navigate to the :doc:`local repository
<get-the-source-code>` and run:

.. code-block:: shell

  python setup.py install -- -- -j2

where you may change 2 to to the number of cores on your system. The build
output is written to a folder :file:`_skbuild` and copied to a system folder
from there.


Developer Mode
~~~~~~~~~~~~~~

In this set-up, we first tell the virtual environment to monitor the source
code directory as an install directory. So, navigate to the :doc:`local
repository <get-the-source-code>` then, depending on which :doc:`virtual
environment </install/virtual-environment>` you chose, do the following:

.. code-block:: shell
  :caption: if you :ref:`use a Conda environment
    <install/virtual-environment:Conda environment>`

  conda develop .

.. code-block:: shell
  :caption: if you :ref:`use Python venv <install/virtual-environment:Python
    venv>`

  pip install virtualenvwrapper
  source venv/bin/virtualenvwrapper.sh
  add2virtualenv .

We now call `cmake <https://cmake.org/>`_ directly to build the `ComPWA backend
<https://github.com/ComPWA/ComPWA>`_:

.. code-block:: shell

  mkdir -p build
  cd build
  cmake ..
  cmake --build . -- -j2

The most important binary build file is the shared library for the
`pycompwa.ui` package. You need to set a symbolic link to this file from the
:file:`pycompwa` source code folder:

.. code-block:: shell

  cd ../pycompwa
  rm -f ui.*.so  # in case you already created a symlink
  ln -s ../build/ui.*.so


Test the installation
~~~~~~~~~~~~~~~~~~~~~

First, navigate out of the main directory of the :doc:`local repository
<get-the-source-code>` in order to make sure that the `pycompwa` we run is the
system installation and not the :file:`pycompwa` folder in the current working
directory. Then, simply launch launch a Python interpreter and run:

.. code-block:: python

  import pycompwa

If you don't get any error messages, all worked out nicely!

For more thorough testing you can run the unit tests:

.. code-block:: shell

  cd tests
  pip install -r requirements.txt
  pytest -m "not slow"

You can now go through the :doc:`/usage/workflow` to learn how to use
:mod:`pycompwa`.
