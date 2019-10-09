How to contribute
=================

.. note::
   
   Note that most of these instructions general and independent of pycompwa, 
   so they are also valid for ComPWA.

How to use git
--------------
If you are new to git, maybe you should read some documentation first. E.g. the
`Manual <https://git-scm.com/docs/user-manual.html>`__, a
`Tutorial <http://rogerdudler.github.com/git-guide/>`__, a 
`CheatSheet <https://services.github.com/on-demand/downloads/github-git-cheat-sheet.pdf>`__.

For your convenience here is the workflow you should use if you want to
contribute:

* Log into GitHub with your account and fork ComPWA
* Get copy of repository: ``git clone git@github.com:YOURACCOUNT/pycompwa.git``
* Add the main repository as a remote: 
  ``git remote add upstream git@github.com:ComPWA/pycompwa.git``

.. note::
   You can name the repository with any name you wish. ``upstream`` is a common
   label for the main repository.
   
   Note the remote from which you cloned the repository initially is by default
   named ``origin`` (here: your fork). A local ``master`` branch is
   automatically checked out from the origin after the clone as well. You can
   list all branches with ``git branch -a``.

The following steps you repeat until your contribution is finished, and can be
added to the main repository.

.. tip::
   Remember to commit frequently to not have single commits with too many
   changes! Rebasing can help you later on to group and alter commit messages,
   so don't worry.

* ... make changes ...
* Check changes: ``git status`` and/or ``git diff``
* Stage updated files for commit:  ``git add -u``
  or add new files ``git add <list of files>``
* Commit changes: ``git commit`` (opens up editor for commit message)
* Enter a meaningful commit message. First line is a overall summary.
  Then a more detailed description if neccessary.
* Synchronize with the changes from the main repository/upstream
  
  * Fetch new changes ``git fetch upstream``
  * Reapply your current branch commits to the head of upstream master branch
    ``git rebase -i upstream/master``
  * At this point conflicts of your and the changes from the main repository
    may occur. If no conflicts appeared then you are finished and can continue
    coding or push your work onto you fork.
    Otherwise repeat these steps until finshed (you can abort the whole rebase
    process via ``git rebase --abort``):
    
    * Review the conflicts (:ref:`VS Code <contribute-vscode>` is great for
      this)
    * Mark them as resolved ``git add <filename>``
    * Continue the rebase ``git rebase --continue``
* Push your changes to your fork: ``git push origin <branchname>``
  This step synchronizes your local and fork branch, but is not required after
  every commit. But it is certainly neccessary once you are ready to merge your
  code into ``upstream``.

  .. tip::
     It can be useful to push your local branch to your fork under a different
     name using ``git push origin <local-branchname>:<remote-branchname>``

Once you think your contribution is finished and can be merged into the main
repository

* Make sure your changes are rebased and pushed into your fork
* Log into GitHub with your account and create a pull request (merge your fork
  branch into the main repository master branch)
* While open, commits pushed to your fork branch will automatically update the
  pull request

.. _contribute-report-issues:

Reporting Issues
----------------
Use the `pycompwa github issues page <https://github.com/ComPWA/pycompwa/issues>`__
to

* report problems/issues 
* file a feature request
* request modifications to existing "unpleasant" code

Please don't hesitate to report any issues, but try make sure not to post
duplicates

We are also very glad if you want to take it into your own hands and contribute
to (py)ComPWA! 

Continuous Integration
----------------------
The master branch is automatically build using TravisCI. Probably it is 
interesting to check out the `log file <https://travis-ci.com/ComPWA/pycompwa>`__
and the projects TravisCI configuration file 
`travisCI.yml <https://github.com/ComPWA/pycompwa/blob/master/.travis.yml>`__.


Code Quality & Conventions
--------------------------

A highly recommended read for learning how to write good code:
**Clean Code, by Robert C. Martin**

Try and follow his advice, and keep in mind the boy scout rule::

  "Leave behind the code cleaner, then you found it"

For the python code we follow the pep8 standard. Available automatic source code
highlighters and formatters are `flake8` and `autopep8`.

Documentation
-------------

Generally try to code in such a way that it is self explanatory and its
documentation is not neccessary. Of course this ideal case is not achieved in
reality, but avoid useless comments such as ``getValue() # get's value``. Also
try to comment only parts, which really need an explanation. Because keeping 
the documentation in sync with the code is crucial, and is a lot of work.

The documentation is built with sphinx using the "read the docs" theme. For the
python code/modules ``sphinx-apidoc`` is used. The comment style is following
the pep8 conventions.