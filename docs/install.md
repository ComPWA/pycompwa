# Installation

:::{warning}

`pycompwa` is no longer maintained. Use the
[ComPWA](https://compwa-org.rtfd.io) packages [QRules](https://qrules.rtfd.io),
[AmpForm](https://ampform.rtfd.io), and
[TensorWaves](https://tensorwaves.rtfd.io) instead!

:::

## Prerequisites

`pycompwa` is [available as a PyPI package](https://pypi.org/). However, since
the `pycompwa.ui` module contains Python bindings to the
[ComPWA backend](https://github.com/ComPWA/ComPWA), you first need to install
certain C++ prerequisites.

What you definitely need to install, is:

- a build tool: [cmake](https://cmake.org/)
- a C++ compiler: [gcc](https://gcc.gnu.org/) or
  [clang](https://clang.llvm.org/)
- [Boost](https://www.boost.org/)
- [Python3](https://www.python.org/downloads/)

The following package are optional:

- [ROOT](https://root.cern.ch/downloading-root) and/or
  [Minuit2](https://root.cern.ch/root/htmldoc/guides/minuit2/Minuit2.html)
- [GSL](https://www.gnu.org/software/gsl/)
- [Geneva](https://www.gemfony.eu/)

It is highly recommended to install ROOT
[with Minuit2 enabled](https://root.cern.ch/building-root). Without it, ComPWA
will have only limited functionality.

:::{hint}

If you have a Linux machine with [apt](https://wiki.debian.org/Apt) and with
administrator rights, you can run the following:

```shell
sudo apt update -y
sudo apt install -y cmake gcc git libboost-all-dev python3
```

ROOT with Minuit2 can be most easily installed by
[downloading a suitable binary for your machine](https://root.cern.ch/downloading-root).

:::

## Installation through pip

Once you have these dependencies installed, you can install `pycompwa` through
[pip](https://pypi.org/project/pip/). You also need to install
[scikit-build](https://scikit-build.readthedocs.io/en/latest/), because it is
used as a build tool for the ComPWA backend:

```shell
pip install scikit-build
pip install pycompwa
```

Et voilà, that's it! You can try out whether the installation works by running:

```python
import pycompwa
```

from the Python interpreter. If that works, you can try out some of the
examples from the {doc}`usage` page.

Note that {command}`pip` **only allows you to install specific releases**. We
therefore recommend following the
{ref}`interactive installation <install:Interactive installation>` procedure
instead.

## Interactive installation

`pycompwa` is an academic research project and is bound to continuously evolve.
We therefore highly recommend installing `pycompwa` from
[the source code](https://github.com/ComPWA/pycompwa), so that you work with
the latest version.

Moreover, since you read as far as this, you must have an interest in
partial-wave analysis, and it is researchers like you who can help bring this
project further! So please, have a look through the following sections to set
up this 'interactive installation':

```{toctree}
:maxdepth: 2

install/source
install/virtual-environment
install/build
```

After that, it's worth having a look at {doc}`develop`!
