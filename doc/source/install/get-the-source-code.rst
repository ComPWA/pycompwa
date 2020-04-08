Get the source code
===================

After you have :ref:`installed the prerequisites <installation:Prerequisites>`,
use `Git <https://git-scm.com/>`_ to get a copy of the `pycompwa source code
<http://github.com/ComPWA/pycompwa>`_. To do so, navigate to a suitable folder
and run:

.. code-block:: shell

  git clone --recurse-submodules git@github.com:ComPWA/pycompwa.git

This will take a few minutes, because the source code for ComPWA and its
submodules will also be downloaded.

After that, there should be a folder called :file:`pycompwa`. We'll call this
folder the **local repository**. If you navigate into it, you can see it has:

* a `pycompwa <https://github.com/ComPWA/pycompwa/tree/master/pycompwa>`_
  folder with Python source code
* a `ComPWA <https://github.com/ComPWA/ComPWA/>`_ folder with C++ source code
* a `requirements.txt <https://github.com/ComPWA/pycompwa/blob/master/requirements.txt>`_
  file listing the Python dependencies
* a `setup.py <https://github.com/ComPWA/pycompwa/blob/master/setup.py>`_ file
  with instructions for :ref:`setuptools <setuptools>`
* a `CMakeLists.txt
  <https://github.com/ComPWA/pycompwa/blob/master/CMakeLists.txt>`_ file for if
  you build with `cmake <https://cmake.org/>`_ (in :ref:`developer mode
  <install/build:Developer Mode>`)

These files will be used in the following steps.
