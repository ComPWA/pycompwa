# cspell:ignore pids
"""Test :mod:`pycompwa.data.naming`."""

from copy import copy
from os.path import dirname, realpath

import pytest

import pycompwa.ui as pwa
from pycompwa.data import convert, exception, naming
from pycompwa.data.naming import _cast_string, _strip_index

SCRIPT_DIR = dirname(realpath(__file__))


pwa.Logging("error")


def create_sample_frame(import_file: str):
    """Import a file with pycompwa and convert it to a `~pandas.DataFrame`."""
    events = pwa.read_ascii_data(import_file)
    frame = convert.events_to_pandas(
        events=events, model=f"{SCRIPT_DIR}/files/kinematics_three.xml"
    )
    return frame


def import_pandas(weights: bool = False):
    """Import the pickled frame."""
    if weights:
        import_file = f"{SCRIPT_DIR}/files/ascii_weights.dat"
    else:
        import_file = f"{SCRIPT_DIR}/files/ascii_noweights.dat"
    return create_sample_frame(import_file)


@pytest.mark.parametrize(
    "kinematics, ids, pids, particles, selection",
    [
        (
            f"{SCRIPT_DIR}/files/kinematics_two.xml",
            [2, 3],
            [22, 111],
            ["gamma", "pi0"],
            ["gamma", "pi0-1"],
        ),
        (
            f"{SCRIPT_DIR}/files/kinematics_three.xml",
            [2, 3, 4],
            [22, "111-1", "111-2"],
            ["gamma", "pi0-1", "pi0-2"],
            ["gamma", "pi0-1", "pi0-2"],
        ),
    ],
)
def test_renames(kinematics, ids, pids, particles, selection):
    """Test rename functions."""
    frame = import_pandas(weights=True)

    # Prepare selection
    frame = frame[selection].copy(deep=True)
    three_particles = len(ids) == 3
    if three_particles:
        with pytest.raises(exception.ConfigurationConflict):
            naming.id_to_particle(frame, kinematics, make_unique=False)
    else:
        frame.rename(columns={"pi0-1": "pi0"}, inplace=True)
    assert frame.pwa.particles == particles

    particle_list = pwa.read_particles(kinematics)

    naming.name_to_pid(frame, particle_list)
    assert frame.pwa.particles == pids

    naming.pid_to_name(frame, particle_list)
    assert frame.pwa.particles == particles

    naming.particle_to_id(frame, kinematics)
    assert frame.pwa.particles == ids

    naming.id_to_particle(frame, kinematics, make_unique=True)
    assert frame.pwa.particles == particles


@pytest.mark.parametrize(
    "input_list, expected",
    [
        (
            ["gamma", "pi0", "pi0"],
            ["gamma", "pi0-1", "pi0-2"],
        ),
        (
            [2, "three", 3],
            [2, "three", 3],
        ),
        (
            [2, 3, 4, 4],
            [2, 3, "4-1", "4-2"],
        ),
        (None, None),
    ],
)
def test_make_values_unique(input_list, expected):
    """Test :func:`.make_values_unique`."""
    unique_list = naming.make_values_unique(input_list)
    assert unique_list == expected


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("2", "gamma"),
        (" 4", " pi0"),
        ("5", "5"),
        ("23", "23"),
        ("3_2", "pi0_gamma"),
        ("f2(1430)", "f2(1430)"),
        ("2,3", "gamma,pi0"),
    ],
)
def test_replace_ids(input_string, expected):
    """Test :func:`.naming.replace_ids`."""
    backup_string = copy(input_string)
    assert expected == naming.replace_ids(
        input_string, f"{SCRIPT_DIR}/files/kinematics_three.xml"
    )
    assert backup_string == input_string


@pytest.mark.parametrize(
    "string, expected",
    [
        (list(), list()),
        (dict(), dict()),
        ("hello", "hello"),
        ("j", complex(0, 1)),
        ("1.1+2j", complex(1.1, 2)),
        ("3.14", float(3.14)),
        ("1.", float(1.0)),
        ("2", int(2)),
    ],
)
def test_cast(string, expected):
    """Test :func:`._cast_string`."""
    assert _cast_string(string) == expected


@pytest.mark.parametrize(
    "string, expected",
    [
        (list(), list()),
        (dict(), dict()),
        (1, 1),
        (3.14, 3.14),
        ("hello", "hello"),
        ("pi0", "pi0"),
        ("pi0-1.2", "pi0-1.2"),
        ("pi0-1", "pi0"),
    ],
)
def test_strip(string, expected):
    """Test :func:`strip_index`."""
    assert _strip_index(string) == expected


@pytest.mark.parametrize(
    "mapping",
    [
        {2: "gamma", 3: "pi0", 4: "pi0"},
        {2: 22, 3: 111, 4: 111},
    ],
)
def test_flip(mapping):
    """Test :func:`.flip_dict`."""
    assert list(naming.flip_dict(mapping).values()) == [[2], [3, 4]]


@pytest.mark.parametrize(
    "mapping, keys, values",
    [
        (
            {2: "gamma", 3: "pi0", 4: "pi0"},
            ["gamma", "pi0-1", "pi0-2"],
            [2, 3, 4],
        ),
        (
            {"gamma": 2, "pi0-1": 3, "pi0-2": 4},
            [2, 3, 4],
            ["gamma", "pi0", "pi0"],
        ),
        (
            {"gamma": 2, "pi0-1": "three"},
            [2, "three"],
            ["gamma", "pi0-1"],
        ),
        (
            {"gamma": 2, "gamma-1.2": 3},
            [2, 3],
            ["gamma", "gamma-1.2"],
        ),
        (
            {2: 22, 3: 111, 4: 111},
            [22, "111-1", "111-2"],
            [2, 3, 4],
        ),
    ],
)
def test_invert(mapping, keys, values):
    """Test :func:`.invert_dict`."""
    result = naming.invert_dict(mapping)
    assert list(result.keys()) == keys
    assert list(result.values()) == values
