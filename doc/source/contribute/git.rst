.. |br| raw:: html

  <br />

How to contribute through Git
-----------------------------

If you are new to Git, it is highly recommended to read through the first few
sections of the `Pro Git book <https://git-scm.com/book/en/v2>`_. It's free and
available in several languages and, most importantly, an easy and worthwhile
read. Understanding `how Git 'thinks'
<https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F>`_ is especially
a huge step towards understanding what Git's terminal commands do, both for
beginners and the more experienced.


Set up your own remote
^^^^^^^^^^^^^^^^^^^^^^

Assuming that you got the pycompwa source code :doc:`like this
</install/get-the-source-code>`, your local repository only has the `main
pycompwa repository <https://github.com/ComPWA/pycompwa>`_ as a `remote
<https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes>`_. We
therefore need to the following.

1. `Sign up <https://github.com/join>`_ or `log into
   <https://github.com/login>`_ GitHub. In the following, we assume that
   ``$ACCOUNT`` is your account name.

2. `Fork the pycompwa repository <https://github.com/ComPWA/pycompwa/fork>`_ so
   that you have a copy in your own GitHub account.

3. Navigate to your local pycompwa repository and change the url of the
   ``origin`` remote: |br|
   ``git set-url git@github.com:$ACCOUNT/pycompwa.git`` |br|
   (this uses the SSH protocol, so you also need to `set your SSH keys
   <https://help.github.com/en/github/authenticating-to-github/managing-commit-signature-verification>`_)

4. Add the main repository as a second remote named ``upstream``: |br|
   ``git remote add upstream git@github.com:ComPWA/pycompwa.git`` |br|
   You can name the repository with any name you wish, but ``upstream`` is just
   a conventional label for the remote of the main repository in a team
   project.

.. note::

  It's definitely reading `this page
  <https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project>`_
  as it explains very well how to work with different remotes!


Creating a pull request
^^^^^^^^^^^^^^^^^^^^^^^

The source code of pycompwa is updated through `pull requests
<https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests>`_.
For this, it is necessary to know `how to work with Git branches
<https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell>`_. The
workflow on GitHub through pull requests is also nicely illustrated in `this
quick and graphical tutorial <https://guides.github.com/introduction/flow>`_!

.. topic:: Typical workflow

  Get the latest source code from the ``upstream`` (the :doc:`old update
  process </install/get-the-source-code>` only gets the updates from the
  ``origin``):

  .. code-block:: shell

    git checkout master
    git fetch --all            # update all remote branches
    git rebase upstream/master # rebase upstream onto local master
    git push -f origin master  # optional: update your fork

  Create a new branch from the updated ``master`` branch:

  .. code-block:: shell

    git checkout -b new_idea master

  Now you can just edit some files and check changes with :command:`git status`
  and/or :command:`git diff`.

  `Stage the modified files
  <https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository#_staging_modified_files>`_
  with either of the following:

  .. code-block:: shell

    git add <some files>
    git add -A  # if you want to stage all, including removed files

  Now commit the changes with either of the following commands and enter a
  meaningful commit message (see :ref:`contribute/git:Commit conventions`):

  .. code-block:: shell

    git commit  # opens an  editor for commit message
    git commit -m "some commit message"

  Repeat this process of editing, staging and committing a few times. Once
  you're satisfied, push the modifications to a new branch on your fork:

  .. code-block:: shell

    git push -u origin new_idea

  You can continue modifying, staging, committing, and pushing. You can even
  create a new branch to try out some other ideas. Once you're satisfied with
  your new idea and want to suggest as a modification to the main repository,
  you're ready to make a pull request. Just go to your fork on GitHub, switch
  to the ``new_idea`` branch and click "New pull request"!

  While the pull request is open, you can still add commits: any commits that
  pushed to the fork branch will immediately appear in the PR.

  .. tip::
    It's safest to commit frequently instead of submitting a PR of just one
    commit. Making frequent 'snapshots' of your work is a safer workflow in
    general. In addition, pycompwa follows a `linear commit history
    <https://help.github.com/en/github/administering-a-repository/requiring-a-linear-commit-history>`_,
    so all commits of your pull request will be `squashed
    <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-merges#squash-and-merge-your-pull-request-commits>`_
    later on.


Commit conventions
^^^^^^^^^^^^^^^^^^

* Please use `conventional commit messages
  <https://www.conventionalcommits.org/>`_: start the commit subject line with
  a semantic keyword (see e.g. `Angular
  <https://github.com/angular/angular/blob/master/CONTRIBUTING.md#type>`_ or
  `these examples
  <https://seesparkbox.com/foundry/semantic_commit_messages>`_,
  followed by `a column <https://git-scm.com/docs/git-interpret-trailers>`_,
  then the message. The subject line should be in imperative mood—just imagine
  the commit to give a command to the code framework. So for instance:
  ``feat: add coverage report tools`` or ``fix: remove ...``. The message
  should be in present tense, but you can add whatever you want there (like
  hyperlinks for references).
* In the master branch, it should be possible to compile and test the framework
  **in each commit**. In your own `topic branches
  <https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows#_topic_branch>`_,
  it is recommended to commit frequently, but `squash or rebase those
  commits <https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History>`_ to
  compilable commits upon submitting a pull request.
