# Get the source code

:::{warning}

`pycompwa` is no longer maintained. Use the
[ComPWA](https://compwa-org.rtfd.io) packages [QRules](https://qrules.rtfd.io),
[AmpForm](https://ampform.rtfd.io), and
[TensorWaves](https://tensorwaves.rtfd.io) instead!

:::

After you have {ref}`installed the prerequisites <install:prerequisites>`, use
[Git](https://git-scm.com/) to get a copy of the
[pycompwa source code](http://github.com/ComPWA/pycompwa). To do so, navigate
to a suitable folder and run:

```shell
git clone --recurse-submodules git@github.com:ComPWA/pycompwa.git
```

This will take a few minutes, because the source code for ComPWA and its
submodules will also be downloaded.

After that, there should be a folder called {file}`pycompwa`. We'll call this
folder the **local repository**. If you navigate into it, you can see it has:

- a [pycompwa](https://github.com/ComPWA/pycompwa/tree/main/src/pycompwa)
  folder with Python source code
- a [ComPWA](https://github.com/ComPWA/ComPWA/) folder with C++ source code
- a
  [requirements.txt](https://github.com/ComPWA/pycompwa/blob/main/requirements.txt)
  file listing the Python dependencies
- a [setup.py](https://github.com/ComPWA/pycompwa/blob/main/setup.py) file with
  instructions for {ref}`setuptools <setuptools>`
- a
  [CMakeLists.txt](https://github.com/ComPWA/pycompwa/blob/main/CMakeLists.txt)
  file for if you build with [cmake](https://cmake.org/) (in
  {ref}`developer mode <install/build:Developer Mode>`)

These files will be used in the following steps.

:::{note}

When new commits are merged into the
[main branch of pycompwa](https://github.com/ComPWA/pycompwa/tree/main), you
need to update your local copy of the source code. It's important that you also
update the submodules:

```shell
git checkout main
git pull --recurse-submodules
```

It's best to have a clean your working tree before you do a
{command}`git pull`. See {doc}`/develop` for more info.

Once you have the update, don't forget to {doc}`rebuild pycompwa <build>`!

:::
