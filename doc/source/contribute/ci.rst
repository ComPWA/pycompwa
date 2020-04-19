Continuous Integration (CI)
---------------------------

Both `pycompwa <https://github.com/ComPWA/pycompwa>`_ and `ComPWA
<https://github.com/ComPWA/ComPWA>`_ are automatically built, tested, and
deployed by `Travis CI <https://travis-ci.com/>`_. You configure the tests in
the `.travis.yml <https://github.com/ComPWA/pycompwa/blob/master/.travis.yml>`_
(see `here <https://docs.travis-ci.com/user/tutorial/>`__ for info on the
syntax). The build logs of all ComPWA repositories can be viewed `here
<https://travis-ci.com/github/ComPWA>`__.

Travis CI builds and tests the source code on each pull request, and whenever a
new commit is added to the master branch. This also creates a complete test
coverage report. Try to keep coverage high by writing more tests (see
:ref:`contribute:pytest`) if coverage decreases. A complete, historical
overview of the code coverage of all ComPWA repositories can be seen `here on
CodeCov <https://codecov.io/gh/ComPWA>`_. Under `files
<https://codecov.io/gh/ComPWA/pycompwa/tree/master/pycompwa>`_ you have a
detailed overview of coverage per module, and you can investigate coverage all
the way down to the source code.

Travis CI also :ref:`builds the documentation <contribute:documentation>` and
runs `Sphinx linkcheck
<https://www.sphinx-doc.org/en/master/_modules/sphinx/builders/linkcheck.html>`_
to verify whether all URLs in the documentation and API are still valid. Once
the pull request is accepted, squashed and merged, the pages are deployed to
`compwa.github.io <https://compwa.github.io/>`_
