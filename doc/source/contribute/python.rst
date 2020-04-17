
Python developer tools
----------------------

Pre-commit
^^^^^^^^^^

An important tool is `pre-commit <https://pre-commit.com/>`_. This will run
certain tests whenever you make a Git commit. To activate, you only have to run
the following once within your virtual environment:

.. code-block:: shell

  pre-commit install

Now, whenever you commit, all tests defined in the `.pre-commit-config.yaml
<https://github.com/ComPWA/pycompwa/blob/master/.pre-commit-config.yaml>`_ file
will be run. Any errors will be fixed where possible and you will have to stage
those new changes. If you do not want to run these tests upon committing, just
use the option :command:`--no-verify`, or :command:`-n`, to skip.

You can also run the checks independently. The command :command:`pre-commit`
will check all staged files and :command:`pre-commit run --file <some files>`
will run over whatever files you are interested in.

Pytest
^^^^^^

We use `pytest <https://docs.pytest.org/>`_ as a testing suite. Simply run:

.. code-block:: shell

  cd tests
  pytest -m "not slow"

Note that we run :command:`pytest` with the flag :command:`-m "not slow"`,
which speeds up the testing, but will make the computed test coverage less
reliable.

If you want to generate a nice graphical overview of which parts of the code
are not covered by the tests, run:

.. code-block:: shell

  pytest --cov-report=html .

and open ``htmlcov/index.html`` in a browser. You can replace the ``.`` with a
specific test of folder to speed things up a bit; the graphical overview is
still helpful.


Jupyter notebook tools
^^^^^^^^^^^^^^^^^^^^^^

Jupyter notebooks aren't the most friendly with regard to Version Control
Systems like Git because in the back-end, a notebook is a JSON file that
changes for instances when you run a cell. There is no simple solution for this
other than to clean the cell output upon saving. Cell output will be striped
automatically with `nbstripout <https://github.com/kynan/nbstripout>`_ upon
committing if you have :ref:`activated pre-commit <contribute:pre-commit>`.

Jupyter offers several other useful extensions that can be activate `like this
<https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html#enabling-disabling-extensions>`_.
If you want to contribute to the example notebooks, the following extensions
are highly recommended:

* `jupyter-autopep8
  <https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/code_prettify/README_autopep8.html>`_
* `ruler
  <https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/ruler/readme.html>`_
* `sphellchecker
  <https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/spellchecker/README.html>`_
