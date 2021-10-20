"""Test :py:class:`pycompwa.data.PwaAccessor`."""


from math import isclose
from os.path import dirname, realpath

import pandas as pd
import pytest

import pycompwa.ui as pwa
from pycompwa.data import _labels, append, convert, exception

SCRIPT_DIR = dirname(realpath(__file__))


def create_sample_frame(import_file: str):
    """Import a file with pycompwa and convert it to a `~pandas.DataFrame`."""
    events = pwa.read_ascii_data(import_file)
    frame = convert.events_to_pandas(
        events=events, model=f"{SCRIPT_DIR}/files/kinematics_three.xml"
    )
    return frame


def import_test_frame(weights: bool = False):
    """Import the pickled frame."""
    if weights:
        import_file = f"{SCRIPT_DIR}/files/ascii_weights.dat"
    else:
        import_file = f"{SCRIPT_DIR}/files/ascii_noweights.dat"
    return create_sample_frame(import_file)


@pytest.mark.parametrize(
    "columns,names",
    [
        (  # just one layer of columns
            ["A", "B", "C"],
            None,
        ),
        (  # wrong momentum labels
            [["A", "B", "C"], ["px", "b"]],
            ["Particles", "Momentum"],
        ),
        (  # three layers
            [["A", "B", "C"], ["px", "b"], [1, 2, 3]],
            ["Particles", "Momentum", "Dummy"],
        ),
    ],
)
def test_validate_wrong(columns, names):
    """Test exception upon validate PWA accessor."""
    if isinstance(columns[0], list):
        columns = pd.MultiIndex.from_product(iterables=columns, names=names)
    frame = pd.DataFrame(columns=columns)
    with pytest.raises(exception.InvalidPwaFormat):
        print(frame.pwa)


@pytest.mark.parametrize(
    "has_weights",
    [
        False,
        True,
    ],
)
def test_weights(has_weights):
    """Test weight related accessors."""
    frame = import_test_frame(weights=has_weights)
    assert frame.pwa.has_weights == has_weights
    if has_weights:
        assert frame.pwa.weights.mean(axis=0) == 0.4
        assert frame.pwa.intensities.mean(axis=0) == 0.4
    else:
        assert frame.pwa.weights is None


@pytest.mark.parametrize(
    "has_weights",
    [
        False,
        True,
    ],
)
def test_labels(has_weights):
    """Test column labels."""
    frame = import_test_frame(weights=has_weights)

    assert frame.pwa.particles == ["gamma", "pi0-1", "pi0-2"]

    gamma = frame["gamma"]
    assert gamma.pwa.particles is None
    assert frame.pwa.weight_label == _labels.WEIGHT

    assert frame.pwa.momentum_labels == _labels.MOMENTA
    assert gamma.pwa.momentum_labels == _labels.MOMENTA

    assert frame.pwa.other_columns == []
    assert gamma.pwa.other_columns == []
    dummy_list = range(len(frame))
    frame.insert(frame.columns.size, "col_0", dummy_list)
    frame.insert(frame.columns.size, "col_n", dummy_list)
    assert frame.pwa.other_columns == ["col_0", "col_n"]


@pytest.mark.parametrize(
    "has_weights",
    [
        False,
        True,
    ],
)
def test_physics(has_weights):
    """Test physics related accessors."""
    frame = import_test_frame(weights=has_weights)
    pions = frame[["pi0-1", "pi0-2"]]
    assert isclose(frame.pwa.energy.mean().sum(axis=0), 3.097, abs_tol=1e-3)
    assert isclose(frame["gamma"].pwa.energy.mean(axis=0), 1.375, abs_tol=1e-3)
    assert isclose(pions.pwa.mass.mean().sum(axis=0), 0.270, abs_tol=1e-3)
    assert isclose(pions["pi0-1"].pwa.mass.mean(axis=0), 0.135, abs_tol=1e-3)
    assert isclose(pions["pi0-1"].pwa.rho.mean(axis=0), 1.197, abs_tol=1e-3)


@pytest.mark.parametrize("has_weights", [False, True])
def test_append(has_weights):
    """Test :py:func:`pycompwa.data.append`."""
    frame = import_test_frame(weights=has_weights)

    frame_pwa = frame.copy()
    frame_pwa_other = frame_pwa.rename(
        columns={"gamma": "two", "pi0-1": "three"}
    )
    frame_pwa_other = frame_pwa_other[["two", "three"]]
    frame_result = append(frame_pwa, frame_pwa_other)
    assert frame_result.pwa.particles == [
        "gamma",
        "pi0-1",
        "pi0-2",
        "two",
        "three",
    ]
    assert not frame_result.pwa.other_columns

    frame_pwa = frame.copy()
    frame_single = pd.DataFrame(list(range(4)), columns=["dummy"])
    frame_result = append(frame_pwa, frame_single)
    assert frame_result.pwa.particles == ["gamma", "pi0-1", "pi0-2"]
    assert frame_result.pwa.other_columns == ["dummy"]

    frame_wrong = pd.DataFrame(list(range(3)))
    with pytest.raises(exception.InvalidPwaFormat):
        append(frame_pwa, frame_wrong)
