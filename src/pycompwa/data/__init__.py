"""Data I/O of the :mod:`pycompwa` package.

This module forms the bridge between ComPWA data samples (or, more generally,
collections of 4-momentum tuples) to the world of :mod:`pandas`.
Additional PWA tools are available through a `dataframe accessor
<https://pandas.pydata.org/pandas-docs/stable/development/extending.html#registering-custom-accessors>`_
named ``pwa`` (see :class:`PwaAccessor`).
"""


__all__ = [
    "PwaAccessor",
    "append",
    "convert",
    "create",
    "io",
    "naming",
]


import pandas as pd
from numpy import sqrt

from . import _labels, convert, create, exception, io, naming


@pd.api.extensions.register_dataframe_accessor("pwa")
class PwaAccessor:
    """:class:`~pandas.DataFrame` accessor for PWA properties.

    Additional namespace to interpret DataFrame as PWA style dataframe, see
    `here
    <https://pandas.pydata.org/pandas-docs/stable/development/extending.html#registering-custom-accessors>`_.
    """

    def __init__(self, pandas_object):
        self._validate(pandas_object)
        self._obj = pandas_object

    @staticmethod
    def _validate(obj):
        columns = obj.columns
        if isinstance(columns, pd.MultiIndex):
            # if multicolumn, test if 2 levels
            columns = columns.levels
            if len(obj.columns.levels) != 2:
                raise exception.InvalidPwaFormat(
                    "Not a PWA data data frame!\n"
                    "pandas.DataFrame must have multicolumns of 2 levels:\n"
                    " - 1st level are the particles names\n"
                    " - 2nd level define the 4-momentum:"
                    f"{_labels.MOMENTA}"
                )
            # then select 2nd columns only
            columns = columns[1]
        # Check if (sub)column names are same as momentum labels
        if not set(_labels.MOMENTA) <= set(columns):
            raise exception.InvalidPwaFormat(
                f"Columns must be {_labels.MOMENTA}"
            )

    @property
    def has_weights(self):
        """Check if dataframe contains weights."""
        return _labels.WEIGHT in self._obj.columns

    @property
    def weights(self):
        """Get list of weights, if available."""
        if not self.has_weights:
            return None
        return self._obj[_labels.WEIGHT]

    @property
    def intensities(self):
        """Alias for :func:`weights` in the case of a fit intensity sample."""
        return self.weights

    @property
    def weight_label(self) -> str:
        """Get the label of the weight column.

        You need to know this string when adding weights.
        """
        return _labels.WEIGHT

    @property
    def momentum_labels(self) -> list:
        """Get list of momentum labels contained in the data frame."""
        if isinstance(self._obj.columns, pd.MultiIndex):
            momentum_labels = self._obj.columns.droplevel(0).unique()
        else:
            momentum_labels = self._obj.columns
        momentum_labels = momentum_labels.to_list()
        if "" in momentum_labels:
            momentum_labels.remove("")
        return momentum_labels

    @property
    def top_columns(self) -> list:
        """Get a list of the top layer column names."""
        columns = self._obj.columns
        if isinstance(columns, pd.MultiIndex):
            columns = self._obj.columns.droplevel(1).unique()
        return columns.to_list()

    @property
    def particles(self) -> list:
        """Get list of non-particle columns contained in the data frame."""
        columns = self._obj.columns
        if not isinstance(columns, pd.MultiIndex):
            return None
        return [
            col
            for col in self.top_columns
            if isinstance(self._obj[col], pd.DataFrame)
            and self._obj[col].columns.unique().to_list() == _labels.MOMENTA
        ]

    @property
    def other_columns(self) -> list:
        """Get list of non-particle column names."""
        particles = self.particles
        if particles is None:
            return list()
        return [
            col
            for col in self.top_columns
            if col not in particles and col != _labels.WEIGHT
        ]

    @property
    def energy(self):
        """Get a dataframe containing only the energies."""
        if isinstance(self._obj.columns, pd.MultiIndex):
            return self._obj.xs(_labels.ENERGY, level=1, axis=1)
        return self._obj[_labels.ENERGY]

    @property
    def p_xyz(self):
        """Get a dataframe containing only the 3-momenta."""
        return self._obj.filter(regex=("p_[xyz]"))
        # ! may conflict with _labels.MOMENTA

    @property
    def rho2(self):
        """**Compute** quadratic sum of the 3-momenta."""
        if isinstance(self._obj.columns, pd.MultiIndex):
            return (self.p_xyz ** 2).sum(axis=1, level=0)
        return (self.p_xyz ** 2).sum(axis=1)

    @property
    def rho(self):
        """**Compute** absolute value of the 3-momenta."""
        return sqrt(self.rho2)

    @property
    def mass2(self):
        """**Compute** the square of the invariant masses."""
        return self.energy ** 2 - self.rho2

    @property
    def mass(self):
        """**Compute** the invariant masses."""
        return sqrt(self.mass2)


def append(pwa_frame: pd.DataFrame, other: pd.DataFrame) -> pd.DataFrame:
    """Append another `~pandas.DataFrame` to a `PWA DataFrame <PwaAccessor>`.

    Parameters:
        pwa_frame: :class:`PWA DataFrame <PwaAccessor>` to which
            you want to append additional columns.
        other: Other `~pandas.DataFrame` from which you take the columns.

    Raises:
        InvalidPwaFormat: If the input ``pwa_frame`` is not a
            :class:`PWA DataFrame <PwaAccessor>`.
    """
    if len(pwa_frame) != len(other):
        raise exception.InvalidPwaFormat(
            f"Cannot merge other DataFrame of length {len(other)} with a "
            f"PWA frame of length {len(pwa_frame)}"
        )
    for col in other.columns:
        pwa_frame[col] = other[col]
    return pwa_frame
