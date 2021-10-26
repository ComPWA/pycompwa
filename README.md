# About pycompwa

[![10.5281/zenodo.3479232](https://zenodo.org/badge/doi/10.5281/zenodo.3479232.svg)](https://doi.org/10.5281/zenodo.3479232)
[![GPLv3+ license](https://img.shields.io/badge/License-GPLv3+-blue.svg)](https://www.gnu.org/licenses/gpl-3.0-standalone.html)

[![GitHub Actions](https://github.com/ComPWA/pycompwa/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/ComPWA/pycompwa/actions/workflows/ci-tests.yml)
[![Codecov](https://codecov.io/gh/ComPWA/pycompwa/branch/main/graph/badge.svg)](https://codecov.io/gh/ComPWA/pycompwa)
[![PyPI package](https://badge.fury.io/py/pycompwa.svg)](https://badge.fury.io/py/pycompwa)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/qrules)](https://pypi.org/project/qrules)
[![Codacy](https://api.codacy.com/project/badge/Grade/adb3ab8d774346b2a3c68f5fa3479c08)](https://app.codacy.com/gh/ComPWA/pycompwa?utm_source=github.com&utm_medium=referral&utm_content=ComPWA/pycompwa&utm_campaign=Badge_Grade_Dashboard)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ComPWA/pycompwa/main.svg)](https://results.pre-commit.ci/latest/github/ComPWA/pycompwa/main)
[![Spelling checked](https://img.shields.io/badge/cspell-checked-brightgreen.svg)](https://github.com/streetsidesoftware/cspell/tree/master/packages/cspell)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort)

pycompwa is a collection of python modules and the python interface to
[ComPWA](https://github.com/ComPWA/ComPWA). ComPWA stands for "Common Partial
Wave Analysis framework".

Analogous to ComPWA, pycompwa's highest focus is also modularity. pycompwa
extends the ComPWA framework with some useful modules:

- [`expertsystem`](https://compwa.github.io/python-modules.html#the-compwa-expert-system)<br>
  A python package that can generate amplitude/intensity model files from
  simple user boundary conditions, such as initial and final state. Currently
  supports the helicity and canonical formalism.

- [`ui`](https://compwa.github.io/python-modules.html#python-ui)<br> The python
  interface to ComPWA, allowing easy steering of ComPWA.

- [`plotting`](https://compwa.github.io/python-modules.html#plotting)<br>
  Facilitates the visualization of data and results, i.e. comparison plots,
  Dalitz plots.

## Installation

Detailed instructions can be found
[here](https://compwa.github.io/installation.html). Make sure the virtual
environment is setup and activated.

### Installation via pypi

```shell
pip install pycompwa
```

### Installation from source

```shell
git clone --recurse-submodules git@github.com:ComPWA/pycompwa.git
cd pycompwa
python setup.py install -j4
```

## Usage

On how to use ComPWA please refer to the
[pycompwa workflow examples](https://compwa.github.io/usage/workflow.html).

## Documentation

The documentation can be found [here](https://compwa.github.io/).
