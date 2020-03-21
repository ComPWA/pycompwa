"""Create an empty `pandas.DataFrame` according to the `~.PwaAccessor`."""


__all__ = [
    'empty_frame',
    'multicolumn',
]


import pandas as pd

from . import _labels
from . import naming


def empty_frame(particle_names: list = None,
                number_of_rows: int = None) -> pd.DataFrame:
    """Create an empty :class:`~pandas.DataFrame`.

    Parameters:
        particle_names (`list`, optional):
            Names that the particle column groups. A simple counter will be
            used if left empty. Note that duplicate particles will receive an
            index.
        number_of_rows (`int`, optional):
            Give the output :class:`~pandas.DataFrame` a certain number of
            rows.
    """
    index = None
    if isinstance(number_of_rows, int):
        index = pd.RangeIndex(number_of_rows)
    multi_column = multicolumn(particle_names)
    return pd.DataFrame(
        index=index,
        columns=multi_column,
    )


def multicolumn(particle_names: list = None):
    """Create a multicolumn.

    The multicolumn complies with the complies with the standards set by the
    :class:`~.PwaAccessor`.
    """
    if particle_names is None:
        return _labels.MOMENTA
    particle_names = naming.make_values_unique(particle_names)
    cols = [(par, mom)
            for par in particle_names
            for mom in _labels.MOMENTA]
    return pd.MultiIndex.from_tuples(
        tuples=cols, names=['Particle', 'Momentum'])
