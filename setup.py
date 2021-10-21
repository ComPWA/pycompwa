import sys

from packaging.version import LegacyVersion
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

setup(
    cmake_args=[
        "-DUSE_GENEVA:BOOL=OFF",
    ],
    cmake_minimum_required_version=CMAKE_MINIMUM,
    setup_requires=SETUP_REQUIRES,
)
