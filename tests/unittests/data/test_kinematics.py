"""Test :py:mod:`pycompwa.data.kinematics`."""


from os.path import dirname, realpath

import pytest

import pycompwa.ui as pwa
from pycompwa.data import kinematics


pwa.Logging('error')

SCRIPT_PATH = dirname(realpath(__file__))


@pytest.mark.parametrize('model, expected', [
    (
        f'{SCRIPT_PATH}/files/kinematics_two.xml',
        {2: 'gamma', 3: 'pi0'},
    ),
    (
        f'{SCRIPT_PATH}/files/kinematics_three.xml',
        {2: 'gamma', 3: 'pi0', 4: 'pi0'},
    ),
])
def test_id_to_name_file(model, expected):
    """Test get ID to name mapping."""
    id_to_name = kinematics.id_to_name_map(model)
    assert id_to_name == expected


def test_id_to_name_other():
    """Test exception of `id_to_name_map`."""
    kin = kinematics.load(f'{SCRIPT_PATH}/files/kinematics_three.xml')
    assert list(kinematics.id_to_name_map(kin).keys()) == [2, 3, 4]
    with pytest.raises(TypeError):
        kinematics.id_to_name_map(666)


@pytest.mark.parametrize('filename', [
    f'{SCRIPT_PATH}/files/ascii_noweights.dat',
    f'{SCRIPT_PATH}/files/ascii_weights.dat',
])
def test_compute(filename):
    """Test conversion from EventCollection to DataSet."""
    event_collection = pwa.read_ascii_data(filename)
    data_set = kinematics.compute(
        event_collection,
        model=f'{SCRIPT_PATH}/files/kinematics_three.xml',
    )
    assert len(data_set.data.keys()) == 16  # kinematics variables
    assert len(data_set.data['mSq_(3,4)']) == 4  # events
