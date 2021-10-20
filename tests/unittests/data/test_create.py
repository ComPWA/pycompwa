"""Test :py:mod:`pycompwa.data.create`."""


import pytest

from pycompwa.data import create


@pytest.mark.parametrize(
    "particles, number_of_rows",
    [
        (["pi+", "D0", "D-"], 100),
        (["gamma", "pi+", "pi-"], None),
        (["gamma", "pi0", "pi0"], None),
        (None, 50),
        (None, None),
    ],
)
def test_empty_frame(particles, number_of_rows):
    """Test creating an empty PWA dataframe."""
    frame = create.pwa_frame(
        particle_names=particles,
        number_of_rows=number_of_rows,
    )
    if number_of_rows is None:
        number_of_rows = 0
    assert not frame.pwa.has_weights
    assert len(frame) == number_of_rows
    if frame.pwa.particles:
        assert len(frame.pwa.particles) == len(particles)
