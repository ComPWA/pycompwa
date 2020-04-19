How to contribute
=================

This page explains some of the tools that we use to work on `pycompwa`.

.. note::

  In order to work on the source code, you need to :doc:`work in a virtual
  environment </install/virtual-environment>` and have `pycompwa` installed in
  :ref:`developer mode <install/build:Developer Mode>`. You can then install
  the developer tools listed under `requirements-dev.txt
  <https://github.com/ComPWA/pycompwa/blob/master/requirements-dev.txt>`_ as
  follows:

  .. code-block:: shell

    pip install -r requirements-dev.txt


Code Quality & Conventions
--------------------------

A highly recommended read for learning how to write good code is `Clean Code
<https://www.goodreads.com/book/show/3735293-clean-code>`_ by Robert C. Martin!
Try and follow his advice, and keep in mind the 'boy scout rule':

    "Leave behind the code cleaner, then you found it"

For the python code we follow the :pep:`8` standard. Available automatic source
code highlighters and formatters are ``flake8`` and ``autopep8``.


.. include:: contribute/git.rst
.. include:: contribute/python.rst
.. include:: contribute/documentation.rst
.. include:: contribute/ci.rst

.. toctree::
    :maxdepth: 1
    :hidden:

    contribute/git
    contribute/python
    contribute/documentation
    contribute/ci


Reporting Issues
----------------
Use the `pycompwa github issues page
<https://github.com/ComPWA/pycompwa/issues>`_ to:

* report problems/issues
* file a feature request
* request modifications to existing "unpleasant" code

Please don't hesitate to report any issues, but try make sure not to post
duplicates.

We are also very glad if you want to take it into your own hands and contribute
to one of the ComPWA repositories! It is easiest, however, if you first propose
the idea as an issue to receive feedback or perhaps even work on an idea
together.
