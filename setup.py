import sys

from packaging.version import LegacyVersion
from setuptools import find_packages
from skbuild.cmaker import get_cmake_version
from skbuild.exceptions import SKBuildError

try:
    from skbuild import setup
except ImportError:
    print("scikit-build is required to build from source.", file=sys.stderr)
    print("Please run:", file=sys.stderr)
    print("", file=sys.stderr)
    print("  python -m pip install scikit-build")
    sys.exit(1)


# Add CMake as a build requirement if cmake is not installed or is too low a
# version
CMAKE_MINIMUM = "3.4"
SETUP_REQUIRES = []
try:
    if LegacyVersion(get_cmake_version()) < LegacyVersion(CMAKE_MINIMUM):
        SETUP_REQUIRES.append("cmake")
except SKBuildError:
    SETUP_REQUIRES.append("cmake")


with open("README.rst") as stream:
    README = stream.read()

setup(
    name="pycompwa",
    version="0.1a6",
    author="Common Partial Wave Analysis",
    author_email="compwa-admin@ep1.rub.de",
    maintainer_email="compwa-admin@ep1.rub.de",
    url="https://github.com/ComPWA/pycompwa",
    project_urls={
        "Tracker": "https://github.com/ComPWA/pycompwa/issues",
        "Changelog": "https://github.com/ComPWA/pycompwa/releases",
        "Documentation": "https://pycompwa.rtfd.io",
        "Source": "https://github.com/ComPWA/pycompwa",
    },
    description="ComPWA: The Common Partial Wave Analysis framework",
    long_description=README,
    long_description_content_type="text/x-rst",
    license="GPLv3 or later",
    keywords=[
        "HEP",
        "PWA",
        "amplitude analysis",
        "partial wave analysis",
        "particle physics",
        "particles",
        "physics",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    cmake_args=[
        "-DUSE_GENEVA:BOOL=OFF",
    ],
    cmake_minimum_required_version=CMAKE_MINIMUM,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"pycompwa": ["particle_list.xml"]},
    zip_safe=False,
    setup_requires=SETUP_REQUIRES,
    tests_require=["pytest"],
    python_requires=">=3.6",
    install_requires=[
        "wheel",
        "pandas>=1.0.0",
        "matplotlib>=2.2.2",
        "numpy>=1.14.5",
        "progress>1.3",
        "uproot3",
        "xmltodict>=0.11.0",
    ],
)
