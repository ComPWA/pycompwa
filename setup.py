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


# Add CMake as a build requirement if cmake is not installed or is too low a
# version
CMAKE_MINIMUM = "3.4"
SETUP_REQUIRES = []
try:
    if LegacyVersion(get_cmake_version()) < LegacyVersion(CMAKE_MINIMUM):
        SETUP_REQUIRES.append('cmake')
except SKBuildError:
    SETUP_REQUIRES.append('cmake')

DATA_FILES = [
    ('pycompwa/', [
        './ComPWA/Physics/particle_list.xml',
    ]),
]

setup(
    name='pycompwa',
    version='0.1-alpha2',
    author='The ComPWA team',
    maintainer_email="compwa-admin@ep1.rub.de",
    url="https://github.com/ComPWA/pycompwa",
    description='ComPWA: The Common Partial Wave Analysis framework',
    long_description="pycompwa is the Python interface of"
    "`ComPWA <https://github.com/ComPWA/ComPWA>`_. "
        "All documentation can be found on "
        "`compwa.github.io <https://compwa.github.io/>`_",
    long_description_content_type='text/x-rst',
    license="GPLv3 or later",
    cmake_args=[
        '-DUSE_GENEVA:BOOL=OFF',
    ],
    cmake_minimum_required_version=CMAKE_MINIMUM,
    packages=find_packages(),
    data_files=DATA_FILES,
    zip_safe=False,
    setup_requires=SETUP_REQUIRES,
    tests_require=['pytest'],
    install_requires=[
        'wheel',
        'pandas>=1.0.0',
        'matplotlib>=2.2.2',
        'numpy>=1.14.5',
        'progress>1.3',
        'uproot',
        'xmltodict>=0.11.0',
    ],
)
