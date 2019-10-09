#!/usr/bin/env python
import sys
from setuptools import find_packages

try:
    from skbuild import setup
except ImportError:
    print('scikit-build is required to build from source.', file=sys.stderr)
    print('Please run:', file=sys.stderr)
    print('', file=sys.stderr)
    print('  python -m pip install scikit-build')
    sys.exit(1)


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pycompwa',
      version='0.0.2',
      author='The ComPWA team',
      maintainer="Peter Weidenkaff",
      maintainer_email="weidenka@uni-mainz.de",
      url="https://github.com/ComPWA/pycompwa",
      description='ComPWA: The common Partial Wave Analysis framework',
      long_description=readme(),
      license="GPLv3 or later",
      #  cmake_args=['-DSOME_FEATURE:BOOL=OFF'],
      cmake_minimum_required_version="3.4",
      packages=find_packages(),
      data_files = [('pycompwa/',['./ComPWA/Physics/particle_list.xml'])],
      zip_safe=False,
      # pytest-runner loads pycompwa from the top-level dir which does
      # not yet contain pybind interface and particle_list.xml. Running pytest
      # indenpentently from the same dir works.
      #  setup_requires=['pytest-runner>=2.0','cmake'],
      setup_requires=['cmake'],
      tests_require=['pytest'],
      install_requires=['wheel', 'numpy>=1.14.5', 'progress>1.3',
                        'xmltodict>=0.11.0', 'matplotlib>=2.2.2', 
                        'uproot'],
      )
