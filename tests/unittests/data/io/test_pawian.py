"""Test :py:mod:`pycompwa.data.import.pawian`."""


import os
from math import isclose
from os.path import dirname, realpath

import pytest

from pycompwa.data import exception
from pycompwa.data.io import pawian

SCRIPT_DIR = dirname(realpath(__file__))


@pytest.mark.parametrize("root_version", [5, 6])
def test_read_hists_file(root_version):
    """Test :func:`~.read_hists_file`."""
    # File loading
    frame_data = pawian.read_hists_file(
        f"{SCRIPT_DIR}/files/pawianHists_ROOT{root_version}.root"
    )
    frame_fit = pawian.read_hists_file(
        f"{SCRIPT_DIR}/files/pawianHists_ROOT{root_version}.root", "fit"
    )
    with pytest.raises(exception.MissingParameter):
        pawian.read_hists_file(
            f"{SCRIPT_DIR}/files/pawianHists_ROOT{root_version}.root", "wrong"
        )

    # Column names
    assert frame_data.pwa.particles == ["gamma", "pi0_1", "pi0_2"]
    assert frame_fit.pwa.particles == ["gamma", "pi0_1", "pi0_2"]
    assert not frame_data.pwa.other_columns
    assert not frame_fit.pwa.other_columns

    # Frame sizes
    number_of_data_events = 21
    phsp_to_data_ratio = 5
    assert len(frame_data) == number_of_data_events
    assert len(frame_fit) == number_of_data_events * phsp_to_data_ratio

    # Weights
    assert not frame_data.pwa.weights
    assert frame_fit.pwa.weights.mean() < 0.95

    # Physics
    pi0_1 = frame_data["pi0_1"]
    pi0_2 = frame_data["pi0_2"]
    assert isclose(frame_data.sum(axis=1).mean(), 3.097, abs_tol=1e-3)
    assert isclose(pi0_1.pwa.mass.mean(), 0.135, abs_tol=1e-3)
    assert isclose(pi0_2.pwa.mass.mean(), 0.135, abs_tol=1e-3)


@pytest.mark.parametrize("has_weights", [False, True])
@pytest.mark.parametrize(
    "particle_interpretation, expected",
    [
        (None, [1, 2, 3]),
        (3, [1, 2, 3]),
        (["gamma", "pi0_1", "pi0_2"], ["gamma", "pi0_1", "pi0_2"]),
    ],
)
def test_read_ascii_no_header(has_weights, particle_interpretation, expected):
    """Test :func:`~.pawian.read_ascii` without header."""
    # Construct filename
    filename = f"{SCRIPT_DIR}/files/"
    if has_weights:
        filename += "pawian_weights.dat"
    else:
        filename += "pawian_noweights.dat"

    # Abort if insufficient info
    if particle_interpretation is None and not has_weights:
        return

    #
    frame = pawian.read_ascii(filename, particle_interpretation)
    assert frame.pwa.particles == expected
    assert (frame.pwa.weights is not None) == has_weights


def test_read_ascii_exceptions():
    """Test exceptions in :func:`~.pawian.read_ascii` without header."""
    # Missing particle interpretation
    with pytest.raises(exception.DataException):
        pawian.read_ascii(f"{SCRIPT_DIR}/files/pawian_noweights.dat", None)
    # Wrong number of particles WITHOUT header
    with pytest.raises(exception.DataException):
        pawian.read_ascii(f"{SCRIPT_DIR}/files/pawian_weights.dat", 4)
    # Wrong number of particles WITH header
    with pytest.raises(exception.DataException):
        pawian.read_ascii(
            f"{SCRIPT_DIR}/../files/ascii_noweights.dat", ["gamma", "pi0"]
        )
    # Correct
    frame = pawian.read_ascii(
        f"{SCRIPT_DIR}/../files/ascii_noweights.dat", ["gamma", "pi0", "pi0"]
    )
    assert frame.pwa.particles == [22, "111-1", "111-2"]


@pytest.mark.parametrize("has_weights", [False, True])
def test_write_ascii(has_weights):
    """Test :func:`~.pawian.write_ascii`."""
    # Construct
    input_file = f"{SCRIPT_DIR}/files/pawian_"
    if has_weights:
        input_file += "weights.dat"
    else:
        input_file += "noweights.dat"
    particles = ["gamma", "pi0-1", "pi0-2"]
    frame_out = pawian.read_ascii(input_file, particles)
    # Export
    output_file = f"{SCRIPT_DIR}/test_pawian.dat"
    pawian.write_ascii(frame_out, output_file)
    # Import
    frame_in = pawian.read_ascii(output_file, particles)
    frame_difference = frame_in - frame_out
    assert isclose(frame_difference.mean().mean(), 0, abs_tol=1e-10)
    os.remove(output_file)
