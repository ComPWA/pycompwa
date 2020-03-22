#!/usr/bin/env python
from packaging.version import LegacyVersion
from skbuild.cmaker import get_cmake_version
from skbuild.exceptions import SKBuildError
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


# Add CMake as a build requirement if cmake is not installed or is too low a
# version
CMAKE_MINIMUM = "3.4"
SETUP_REQUIRES = []
try:
    if LegacyVersion(get_cmake_version()) < LegacyVersion(CMAKE_MINIMUM):
        SETUP_REQUIRES.append('cmake')
except SKBuildError:
    SETUP_REQUIRES.append('cmake')

setup(name='pycompwa',
      version='0.1.00',
      author='The ComPWA team',
      maintainer="Peter Weidenkaff",
      maintainer_email="weidenka@uni-mainz.de",
      url="https://github.com/ComPWA/pycompwa",
      description='ComPWA: The common Partial Wave Analysis framework',
      long_description=readme(),
      license="GPLv3 or later",
      #  cmake_args=['-DSOME_FEATURE:BOOL=OFF'],
      cmake_minimum_required_version=CMAKE_MINIMUM,
      packages=find_packages(),
      data_files=[('pycompwa/', ['./ComPWA/Physics/particle_list.xml'])],
      zip_safe=False,
      setup_requires=SETUP_REQUIRES,
      tests_require=['pytest'],
      install_requires=['wheel', 'numpy>=1.14.5', 'progress>1.3',
                        'xmltodict>=0.11.0', 'matplotlib>=2.2.2',
                        'uproot'],
      )
