Documentation
-------------

Generally try to code in such a way that it is self explanatory and its
documentation is not necessary. Of course this ideal case is not achieved in
reality, but avoid useless comments such as ``getValue() # gets value``. Also
try to comment only parts, which really need an explanation. Because keeping
the documentation in sync with the code is crucial, and is a lot of work.

The documentation is built with sphinx using the "read the docs" theme. For the
python code/modules ``sphinx-apidoc`` is used. The comment style is following
the ``doc8`` conventions.

You can build the documentation locally as follows. In your Conda environment,
navigate to the pycompwa repository, then do:

.. code-block:: shell

  cd doc
  pip install -r requirements.txt
  make html

Now, open the file ``doc/source/_build/html/index.html``.
