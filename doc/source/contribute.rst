.. |br| raw:: html

  <br />

How to contribute
=================

.. _DeveloperMode:

Developer mode
--------------

If you want to develop new functionality for pycompwa, installing pycompwa as a Conda package will not suffice: you will have to **build from source**. In this 'developer mode', you still work in a Conda environment (see :ref:`Installation <Installation>`), but now you install the pycompwa package from the cloned repository using `conda-develop <https://docs.conda.io/projects/conda-build/en/latest/resources/commands/conda-develop.html>`__, so that any changes you make in the source code immediately have effect.

First, create a new Conda environment for pycompwa with the necessary packages:

.. code-block:: shell

  conda create --name compwa python jupyter pytest

Now, clone the pycompwa repository recursively to some suitable folder (you can omit the ``<PYCOMPWA_SOURCE_PATH>``):

.. code-block:: shell

  git clone --recurse-submodules git@github.com:ComPWA/pycompwa.git <PYCOMPWA_SOURCE_PATH>

Then, navigate into the cloned repository under ``<PYCOMPWA_SOURCE_PATH>`` and install the required Python packages:

.. code-block:: shell

  pip install -r requirements.txt

You can now build the pycompwa package from source:

.. code-block:: shell

  mkdir -p build
  cd build
  cmake ..
  make -j4

You will then need to set some symbolic links to the Python module of pycompwa:

.. code-block:: shell

  cd pycompwa
  ln -s ../build/ui.*.so .
  ln -s ../ComPWA/Physics/particle_list.xml .

Finally, you can tell Conda where to locate the pycompwa package, so that the Python interpreter understand the ``import pycompwa`` command. You do this with:

.. code-block:: shell

  conda develop <PATH_TO_pycompwa>

where ``<PATH_TO_pycompwa>`` refers to the absolute or relative path of the cloned pycompwa repository.

How to contribute through Git
-----------------------------

.. note::

  Note that most of the following instructions are general and independent of pycompwa, so they are also valid for ComPWA.

If you are new to git, maybe you should read some documentation first, such as the
`Git Manual <https://git-scm.com/docs/user-manual.html>`__,
`Tutorial <http://rogerdudler.github.com/git-guide/>`__, a
`CheatSheet <https://services.github.com/on-demand/downloads/github-git-cheat-sheet.pdf>`__.
The `Git Pro <https://git-scm.com/book/en/v2>`__ book particularly serves as a great, free overview that is a nice read for both beginners and more experienced users.

For your convenience, here is the Git workflow you should use if you want to contribute:

1. Log into GitHub with your account and fork the ComPWA repository
2. Get a local copy of repository: |br|
   ``git clone git@github.com:YOURACCOUNT/pycompwa.git`` |br|
   (this uses the SSH protocol, so you need to `set your SSH keys <https://help.github.com/en/github/authenticating-to-github/managing-commit-signature-verification>`__ first)
3. Add the main repository as a second remote called ``upstream``: |br|
   ``git remote add upstream git@github.com:ComPWA/pycompwa.git``

.. note::
  You can name the repository with any name you wish: ``upstream`` is just a common label for the main repository.

  Note that the remote from which you cloned the repository is named ``origin`` by default (here: your fork). A local ``master`` branch is automatically checked out from the origin after the clone. You can list all branches with ``git branch -a``.

You repeat the following steps until your contribution is finished. Only then can your contributions be added main repository through a `pull request <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests>`__ (PR).

* ... edit some files ...
* Check changes: ``git status`` and/or ``git diff``
* Stage updated files for commit: |br|
  ``git add -u`` or add new files ``git add <list of files>``
* Commit changes: ``git commit`` (opens up editor for commit message)
* Enter a meaningful commit message. First line is a overall summary. Then, if necessary, skip one line and add a more detailed description form the third line on.
* Synchronize with the changes from the main repository/upstream:

  - Fetch new changes: |br|
    ``git fetch upstream``
  - Re-apply your current branch commits to the head of the ``upstream`` master branch: |br|
    ``git rebase -i upstream/master``
  - At this point, conflicts between your changes and those from the main ``upstream`` repository may occur. If no conflicts appeared, then you are finished and you can continue coding or push your work onto you fork. Otherwise repeat these steps until you're done (you can abort the whole rebase process via ``git rebase --abort``):

    + Review the conflicts (`VS Code <https://code.visualstudio.com/>`__ is a great tool for this)
    + Mark them as resolved ``git add <filename>``
    + Continue the rebase ``git rebase --continue``
* Push your changes to your fork: |br|
  ``git push origin <branchname>`` |br|
  This step 'synchronizes' your local branch and the branch in your fork. It is not required after every commit, but it is certainly necessary once you are ready to merge your code into ``upstream``.

.. tip::
  Remember to commit frequently instead of submitting a PR of just one commit. Making frequent snapshots (commits) of your work is safer workflow in general. Later on, rebasing can help you to group and alter commit messages, so don't worry.

.. tip::
  It can be useful to push your local branch to your fork under a different name using: |br|
  ``git push origin <local-branchname>:<remote-branchname>``

Once you think your contribution is finished and can be merged into the main repository:

* Make sure your the latest commits from the ``upstream/master`` are rebased onto your new branch and pushed to your fork
* Log into GitHub with your account and create a PR. This is a request to merge the changes in your fork branch with the ``master`` branch of the pycompwa or ComPWA repository.
* While the PR is open, commits pushed to the fork branch behind your PR will immediately appear in the PR.


.. _contribute-report-issues:

Reporting Issues
----------------
Use the `pycompwa github issues page <https://github.com/ComPWA/pycompwa/issues>`__ to:

* report problems/issues
* file a feature request
* request modifications to existing "unpleasant" code

Please don't hesitate to report any issues, but try make sure not to post duplicates.

We are also very glad if you want to take it into your own hands and contribute to (py)ComPWA!

Continuous Integration (CI)
---------------------------
The master branch is automatically build using TravisCI. Probably it is interesting to check out the `log file <https://travis-ci.com/ComPWA/pycompwa>`__ and the projects TravisCI configuration file `travisCI.yml <https://github.com/ComPWA/pycompwa/blob/master/.travis.yml>`__.


Code Quality & Conventions
--------------------------
A highly recommended read for learning how to write good code: |br|
**Clean Code, by Robert C. Martin**

Try and follow his advice, and keep in mind the 'boy scout rule'::

  "Leave behind the code cleaner, then you found it"

For the python code we follow the `pep8 standard <https://www.python.org/dev/peps/pep-0008/>`__. Available automatic source code highlighters and formatters are `flake8` and `autopep8`.

Documentation
-------------
Generally try to code in such a way that it is self explanatory and its documentation is not necessary. Of course this ideal case is not achieved in reality, but avoid useless comments such as ``getValue() # gets value``. Also try to comment only parts, which really need an explanation. Because keeping the documentation in sync with the code is crucial, and is a lot of work.

The documentation is built with sphinx using the "read the docs" theme. For the python code/modules ``sphinx-apidoc`` is used. The comment style is following the ``pep8`` conventions.

You can build the documentation locally as follows. In your Conda environment, navigate to the pycompwa repository, then do:

.. code-block:: shell

  cd doc
  pip install -r requirements.txt
  make html

Now, open the file ``doc/source/_build/html/index.html``.
