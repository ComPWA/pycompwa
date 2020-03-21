"""Exceptions of the :mod:`pycompwa.data` module."""


__all__ = [
    'DataException',
    'InvalidPwaFormat',
]


class DataException(Exception):
    """General exception for the :mod:`pycompwa.data` module."""


class InvalidPwaFormat(DataException):
    """Raised if :class:`pandas.DataFrame` is not PWA-formatted.

    See :class:`~.PwaAccessor` for how the :class:`~pandas.DataFrame` should
    be formatted.
    """
