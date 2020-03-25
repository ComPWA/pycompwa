"""Exceptions of the :mod:`pycompwa.data` module."""


__all__ = [
    'DataException',
    'ConfigurationConflict',
    'InvalidPwaFormat',
]


class DataException(Exception):
    """General exception for the :mod:`pycompwa.data` module."""


class ConfigurationConflict(DataException):
    """Configuration file (e.g. XML file) conflicts with data input."""


class InvalidPwaFormat(DataException):
    """Raised if :class:`pandas.DataFrame` is not PWA-formatted.

    See :class:`~.PwaAccessor` for how the :class:`~pandas.DataFrame` should
    be formatted.
    """
