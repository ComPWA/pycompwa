Documentation
-------------

Sphinx
^^^^^^

The source code for the `compwa.github.io website <https://compwa.github.io/>`_
is located in the `doc/source
<https://github.com/ComPWA/pycompwa/tree/master/doc/source>`_ folder of the
repository, so it is easy to contribute to the website as well! Simply run the
following to build the whole website locally:

.. code-block:: shell

  cd doc
  pip install -r requirements.txt  # also installed from requirements-dev.txt
  make html

Now, open the file :file:`doc/source/_build/html/index.html` to view the main
page.

The :command:`make html` does three things:

1. The Jupyter notebooks from the `examples
   <https://github.com/ComPWA/pycompwa/tree/master/examples>`_ folder are
   copied and converted to :file:`.rst` files by `nbsphinx
   <https://nbsphinx.readthedocs.io/>`_.
2. `sphinx-apidoc
   <https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html>`_ create API
   pages in :file:`.rst` format from the `pycompwa` module.
3. Finally, all :file:`.rst` files are read and converted to HTML pages by
   `sphinx-build
   <https://www.sphinx-doc.org/en/master/man/sphinx-build.html>`_.

Another useful 'target' is `linkcheck
<https://www.sphinx-doc.org/en/master/_modules/sphinx/builders/linkcheck.html>`_.
The command :code:`make linkcheck` verifies whether all URLs in both
documentation and API are still valid.


reStructuredText
^^^^^^^^^^^^^^^^

In all three steps, documentation is written in `reStructuredText
<https://docutils.sourceforge.io/rst.html>`_ (:file:`.rst` or reST). This is a
mark-up language like `Markdown <https://www.markdownguide.org/>`_ that allows
for more technical and cross-referenced documentation (see a short comparison
`here <https://www.zverovich.net/2016/06/16/rst-vs-markdown.html>`__).
Unfortunately, reST is a bit harder to master (particularly the concept of
`roles
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html>`_ and
`directives
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html>`_),
but `this primer by Sphinx
<http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ is a
good starting point. The concept of `domains
<http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-python-domain>`_
is also important for the API.


Python docstrings and API
^^^^^^^^^^^^^^^^^^^^^^^^^

Python code is documented with `docstrings
<https://www.python.org/dev/peps/pep-0257/>`_. These docstrings are important
and quite powerful because:

* They are embedded into the code (see the built-in :func:`help` function).

* They force the developer to consider usage. This is also why we apply
  :pep:`257` and related docstring conventions quite strictly through `flake8
  <https://flake8.pycqa.org/en/latest/>`_ and `pylint
  <https://www.pylint.org/>`_ at :ref:`pre-commit <contribute:pre-commit>`
  stage.

* They are rendered in the API that is :ref:`built by sphinx
  <contribute:Sphinx>`.

The latter fact is especially noteworthy: it means that the docstrings can
reference to pages and sections from the website! For this, the `:doc:
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-doc>`_
and `:ref:
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-ref>`_
roles are particularly useful.

Another cool thing is that you can refer to external APIs from both the
docstrings and the documentation pages as well! This is handled automatically
through `intersphinx
<https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>`_ (you
may have to add more URLs to APIs in the `conf.py
<https://github.com/ComPWA/pycompwa/blob/master/doc/source/conf.py>`_ file). In
addition, the `primary_domain
<https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-primary_domain>`_
has been set to :code:`py`, and the `default_role
<https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-default_role>`_
to :code:`py:obj`, which means that you can for instance simplify references to
external APIs and the internal API like this:

.. code-block:: rst

  `dict`
  `~pandas.DataFrame`
  :func:`.create.pwa_frame`

This automatically creates links to `dict`, `~pandas.DataFrame`, and
:func:`.create.pwa_frame`, respectively. The meaning of the :code:`~` and
:code:`.` is explained `here
<http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cross-referencing-python-objects>`__
(at the end).
