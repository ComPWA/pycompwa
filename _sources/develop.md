# Help developing

<!-- cspell:ignore autopep htmlcov nbstripout -->

:::{warning}

`pycompwa` is no longer maintained. Use the
[ComPWA](https://compwa-org.rtfd.io) packages [QRules](https://qrules.rtfd.io),
[AmpForm](https://ampform.rtfd.io), and
[TensorWaves](https://tensorwaves.rtfd.io) instead!

:::

:::{tip}

For more info, see
[the developing page of the ComPWA organization](https://compwa-org.readthedocs.io/en/stable/develop.html).

:::

(python-dev-tools)=

## Python developer tools

For contributing to pycompwa, we recommend you also install the packages listed
under {download}`requirements-dev.txt <../requirements-dev.txt>`. In the Conda
environment you created for pycompwa:

```shell
conda install --file requirements-dev.txt
```

An important tool there is [pre-commit](https://pre-commit.com/). This will run
certain tests locally when you make a Git commit. To activate, run the
following after cloning:

```shell
pre-commit install
```

Now, whenever you commit, all tests defined in the `.pre-commit-config.yaml`
fill be run. Any errors will be fixed where possible and you will have to stage
those new changes. You can also first test all staged files with the command
`pre-commit`. If, however, you do not want to run these tests upon committing,
just use the option `--no-verify`, or `-n`, skip.

A tool that tests _all_ relevant files is `tox`. The tests that `tox` runs are
defined in the `tox.ini` file in the main directory.

You also check the coverage of the unit tests:

```shell
cd tests
pytest
```

Now you can find a nice graphical overview of which parts of the code are not
covered by the tests by opening `htmlcov/index.html`!

If you want to speed up the tests you can run `pytest` with the flag
`-m "not slow"`. Note, however, that in that case, the test coverage is not
reliable.

## Jupyter notebook tools

Jupyter notebooks aren't the most friendly with regard to Version Control
Systems like Git because in the back-end, a notebook is a JSON file that
changes for instances when you run a cell. There is no simple solution for this
other than to clean the cell output upon saving. You can automatize this with
[nbstripout](https://github.com/kynan/nbstripout) if you have activated
`pre-commit` (see {ref}`python-dev-tools`).

Jupyter offers several other useful extensions that can be activate
[like this](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html#enabling-disabling-extensions)
If you want to contribute to the example notebooks, make sure to check out the
following extensions:

- [jupyter-autopep8](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/code_prettify/README_autopep8.html)
- [ruler](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/ruler/readme.html)

### How to contribute through Git

:::{note}

Note that most of the following instructions are general and independent of
pycompwa, so they are also valid for ComPWA.

:::

:::

If you are new to git, maybe you should read some documentation first, such as
the [Git Manual](https://git-scm.com/docs/user-manual.html),
[Tutorial](http://rogerdudler.github.io/git-guide/), a
[CheatSheet](https://services.github.com/on-demand/downloads/github-git-cheat-sheet.pdf).
The [Git Pro](https://git-scm.com/book/en/v2) book particularly serves as a
great, free overview that is a nice read for both beginners and more
experienced users.

For your convenience, here is the Git workflow you should use if you want to
contribute:

1. Log into GitHub with your account and fork the ComPWA repository
2. Get a local copy of repository: <br>
   `git clone git@github.com:YOUR_ACCOUNT/pycompwa.git` <br> (this uses the SSH
   protocol, so you need to
   [set your SSH keys](https://help.github.com/en/github/authenticating-to-github/managing-commit-signature-verification)
   first)
3. Add the main repository as a second remote called `upstream`: <br>
   `git remote add upstream git@github.com:ComPWA/pycompwa.git`

:::{note}

:::

can name the repository with any name you wish: `upstream` is just a common
label for the main repository.

Note that the remote from which you cloned the repository is named `origin` by
default (here: your fork). A local `main` branch is automatically checked out
from the origin after the clone. You can list all branches with
`git branch -a`.

:::

:::

You repeat the following steps until your contribution is finished. Only then
can your contributions be added main repository through a
[pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)
(PR).

- ... edit some files ...

- Check changes: `git status` and/or `git diff`

- Stage updated files for commit: <br> `git add -u` or add new files
  `git add <list of files>`

- Commit changes: `git commit` (opens up editor for commit message)

- Enter a meaningful commit message. First line is a overall summary. Then, if
  necessary, skip one line and add a more detailed description form the third
  line on.

- Synchronize with the changes from the main repository/upstream:

  - Fetch new changes: <br> `git fetch upstream`

  - Re-apply your current branch commits to the head of the `upstream` main
    branch: <br> `git rebase -i upstream/main`

  - At this point, conflicts between your changes and those from the main
    `upstream` repository may occur. If no conflicts appeared, then you are
    finished and you can continue coding or push your work onto you fork.
    Otherwise repeat these steps until you're done (you can abort the whole
    rebase process via `git rebase --abort`):

    - Review the conflicts ([VS Code](https://code.visualstudio.com/) is a
      great tool for this)
    - Mark them as resolved `git add <filename>`
    - Continue the rebase `git rebase --continue`

- Push your changes to your fork: <br> `git push origin <branch-name>` <br>
  This step 'synchronizes' your local branch and the branch in your fork. It is
  not required after every commit, but it is certainly necessary once you are
  ready to merge your code into `upstream`.

:::{tip}

Remember to commit frequently instead of submitting a PR of just one commit.
Making frequent snapshots (commits) of your work is safer workflow in general.
Later on, rebasing can help you to group and alter commit messages, so don't
worry.

:::

:::{tip}

It can be useful to push your local branch to your fork under a different name
using: <br> `git push origin <local-branch-name>:<remote-branch-name>`

:::

Once you think your contribution is finished and can be merged into the main
repository:

- Make sure your the latest commits from the `upstream/main` are rebased onto
  your new branch and pushed to your fork
- Log into GitHub with your account and create a PR. This is a request to merge
  the changes in your fork branch with the `main` branch of the pycompwa or
  ComPWA repository.
- While the PR is open, commits pushed to the fork branch behind your PR will
  immediately appear in the PR.

## Commit conventions

- In the main branch, it should be possible to compile and test the framework
  **in each commit**. In your own topic branches, it is recommended to commit
  frequently (WIP keyword), but
  [squash those commits](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)
  to compilable commits upon submitting a merge request.
- Please use
  [conventional commit messages](https://www.conventionalcommits.org/): start
  the commit subject line with a semantic keyword (see e.g.
  [Angular](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#type)
  or
  [these examples](https://seesparkbox.com/foundry/semantic_commit_messages),
  followed by [a column](https://git-scm.com/docs/git-interpret-trailers), then
  the message. The subject line should be in imperative mood—just imagine the
  commit to give a command to the code framework. So for instance:
  `feat: add coverage report tools` or `fix: remove ...`. The message should be
  in present tense, but you can add whatever you want there (like hyperlinks
  for references).

(contribute-report-issues)=

### Reporting Issues

Use the
[pycompwa github issues page](https://github.com/ComPWA/pycompwa/issues) to:

- report problems/issues
- file a feature request
- request modifications to existing "unpleasant" code

Please don't hesitate to report any issues, but try make sure not to post
duplicates.

We are also very glad if you want to take it into your own hands and contribute
to (py)ComPWA!

### Continuous Integration (CI)

The main branch is automatically build using GitHub Actions. Probably it is
interesting to check out the
[log file](https://github.com/ComPWA/pycompwa/actions/workflows/ci-tests.yml)
and the workflow files under
[.github/workflows](https://github.com/ComPWA/pycompwa/blob/main/.github/workflows).

A code coverage report is generated for each pull request. Try to keep coverage
high by writing new tests if coverage decreases. You can see an overview
pycompwa's coverage [here](https://codecov.io/gh/ComPWA/pycompwa). Under
[files](https://codecov.io/gh/ComPWA/pycompwa/tree/master/pycompwa) you have a
detailed overview of coverage per module, and you can investigate coverage all
the way down to the source code.

### Code Quality & Conventions

A highly recommended read for learning how to write good code: <br> **Clean
Code, by Robert C. Martin**

Try and follow his advice, and keep in mind the 'boy scout rule':

```{epigraph}
"Leave behind the code cleaner, then you found it"

-- "Uncle" Bob
```

For the python code we follow the
[pep8 standard](https://www.python.org/dev/peps/pep-0008/). Available automatic
source code highlighters and formatters are `flake8` and `autopep8`.

### Documentation

Generally try to code in such a way that it is self explanatory and its
documentation is not necessary. Of course this ideal case is not achieved in
reality, but avoid useless comments such as `getValue() # gets value`. Also try
to comment only parts, which really need an explanation. Because keeping the
documentation in sync with the code is crucial, and is a lot of work.

The documentation is built with sphinx using the "read the docs" theme. For the
python code/modules `sphinx-apidoc` is used. The comment style is following the
`doc8` conventions.

You can build the documentation locally as follows. In your Conda environment,
navigate to the pycompwa repository, then do:

```shell
cd docs
conda install --file requirements.txt
make html
```

Now, open the file `docs/_build/html/index.html`.
