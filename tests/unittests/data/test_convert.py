# cspell:ignore iloc
"""Test :mod:`pycompwa.data.convert`."""

from math import isclose, sqrt
from os.path import dirname, realpath

import pytest

import pycompwa.ui as pwa
from pycompwa.data import _labels, append, convert, exception, naming

SCRIPT_DIR = dirname(realpath(__file__))


pwa.Logging("error")


def import_events(weights: bool = False):
    """Import the data sample as `~.EventCollection`."""
    if weights:
        import_file = f"{SCRIPT_DIR}/files/ascii_weights.dat"
    else:
        import_file = f"{SCRIPT_DIR}/files/ascii_noweights.dat"
    return pwa.read_ascii_data(import_file)


def import_pandas(weights: bool = False):
    """Import the pickled frame."""
    events = import_events(weights)
    frame = convert.events_to_pandas(
        events=events, model=f"{SCRIPT_DIR}/files/kinematics_three.xml"
    )
    return frame


@pytest.mark.parametrize("has_weights", [False, True])
def test_data_set_to_pandas(has_weights):
    """Test :func:`~.data_set_to_pandas`."""
    events = import_events(has_weights)
    data_set = pwa.compute_kinematic_variables(
        events, xml_filename=f"{SCRIPT_DIR}/files/kinematics_three.xml"
    )
    frame = convert.data_set_to_pandas(data_set)

    with pytest.raises(exception.InvalidPwaFormat):
        print(frame.pwa.particles)

    variable_names = frame.columns.to_list()
    assert "mSq_(2,3)" in variable_names
    if has_weights:
        assert len(variable_names) == 17
        assert frame[_labels.WEIGHT].iloc[-1] == 0.7
    else:
        assert len(variable_names) == 16


@pytest.mark.parametrize("has_weights", [False, True])
def test_events_to_pandas(has_weights):
    """Test :func:`~.events_to_pandas`."""
    events = import_events(has_weights)
    with pytest.raises(exception.ConfigurationConflict):
        convert.events_to_pandas(
            events, f"{SCRIPT_DIR}/files/kinematics_two.xml"
        )

    frame = convert.events_to_pandas(events)
    assert frame.pwa.particles == [22, "111-1", "111-2"]
    del frame

    xml_filename = f"{SCRIPT_DIR}/files/kinematics_three.xml"
    frame = convert.events_to_pandas(events, model=xml_filename)
    assert frame.pwa.particles == ["gamma", "pi0-1", "pi0-2"]

    data_set = pwa.compute_kinematic_variables(events, xml_filename)
    frame_kinematics = convert.data_set_to_pandas(data_set)
    append(frame, frame_kinematics)
    assert len(frame.pwa.other_columns) == 16
    assert "theta_2_4_vs_3" in frame.pwa.other_columns
    assert isclose(sqrt(frame["mSq_(2,3,4)"].mean()), 3.097, abs_tol=1e-3)


@pytest.mark.parametrize("has_weights", [False, True])
def test_pandas_to_events(has_weights):
    """Test pandas_to_events."""
    frame = import_pandas(has_weights)
    forward_map = {2: "one", 3: "two", 4: "three"}
    backward_map = {value: key for key, value in forward_map.items()}
    frame.rename(columns=forward_map, inplace=True)

    model_file = f"{SCRIPT_DIR}/files/kinematics_three.xml"
    with pytest.raises(Exception):
        convert.pandas_to_events(frame, model_file)
    frame.rename(columns=backward_map, inplace=True)
    naming.particle_to_id(frame, model_file)
    events = convert.pandas_to_events(frame, model_file)
    event_list = events.events
    last_event = event_list[-1]
    if has_weights:
        assert last_event.weight == 0.7
    else:
        assert last_event.weight == 1.0
