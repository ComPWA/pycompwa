"""Tools for naming and renaming column names of a :class:`pandas.DataFrame`.

The :class:`~pandas.DataFrame` has to be formatted according to the conventions
set by the :class:`~.PwaAccessor`. Also contains tools for inverting
:class:`dict` objects.
"""


__all__ = [
    "flip_dict",
    "id_to_particle",
    "invert_dict",
    "make_values_unique",
    "name_to_pid",
    "particle_to_id",
    "pid_to_name",
    "replace_ids",
]


import re

import pandas as pd

import pycompwa.ui as pwa

from . import exception

_SEPARATOR = "-"


def id_to_particle(
    frame: pd.DataFrame, model: str, make_unique: bool = False
) -> pd.DataFrame:
    """Rename columns from final state IDs to particle names."""
    id_to_name = _id_to_name(model)
    if not make_unique:
        final_states = list(id_to_name.values())
        if len(final_states) != len(set(final_states)):
            raise exception.ConfigurationConflict(
                f"The final state {final_states} defined in XML file "
                f'"{model}" contains identical particles. Use '
                "make_unique=True to enable applying this mapping."
            )
    else:
        id_to_name = {
            value: key for key, value in invert_dict(id_to_name).items()
        }
    frame.rename(columns=id_to_name, inplace=True)
    return frame


def particle_to_id(frame: pd.DataFrame, model: str) -> pd.DataFrame:
    """Rename particles into their final state IDs."""
    id_to_name = _id_to_name(model)
    name_to_id = invert_dict(id_to_name)
    frame.rename(columns=name_to_id, inplace=True)
    return frame


def name_to_pid(frame: pd.DataFrame, particle_list) -> pd.DataFrame:
    """Rename PIDs to their corresponding particle names."""
    mapping = dict()
    for name in frame.pwa.particles:
        try:
            pid = particle_list.name_to_pid(name)
        except RuntimeError:
            pid = particle_list.name_to_pid(_strip_index(name))
            pid = str(pid) + _SEPARATOR + name.split(_SEPARATOR)[-1]
        mapping[name] = pid
    frame.rename(columns=mapping, inplace=True)
    return frame


def pid_to_name(frame: pd.DataFrame, particle_list) -> pd.DataFrame:
    """Rename particle names to their corresponding PID."""
    mapping = dict()
    for pid in frame.pwa.particles:
        try:
            name = particle_list.pid_to_name(int(pid))
        except (RuntimeError, ValueError):
            name = particle_list.pid_to_name(int(_strip_index(pid)))
            name = str(name) + _SEPARATOR + pid.split(_SEPARATOR)[-1]
        mapping[pid] = name
    frame.rename(columns=mapping, inplace=True)
    return frame


def replace_ids(string: str, model: str):
    """Replace all IDs in a string by particle names.

    Only whole words are replaced, so the final state IDs have to be separated
    by word boundaries or underscores.
    """
    id_to_name = _id_to_name(model)
    new_string = string
    for final_state_id, name in id_to_name.items():
        final_state_id = str(final_state_id)
        match = re.compile(r"(?<![^\W_])" + final_state_id + r"(?![^\W_])")
        new_string = match.sub(name, new_string)
    return new_string


def make_values_unique(values: list) -> list:
    """Append indices to duplicate entries in a `list`."""
    if values is None:
        return values
    new_dict = dict(zip(range(len(values)), values))
    inverted_dict = invert_dict(new_dict)
    return list(inverted_dict.keys())


def invert_dict(mapping: dict) -> dict:
    """Invert a `dict` by appending an index to duplicate values."""
    stripped_keys = [_strip_index(val) for val in mapping.keys()]

    def safe_strip(value):
        stripped_value = _cast_string(_strip_index(value))
        if stripped_keys.count(stripped_value) > 1:
            return stripped_value
        return value

    inversion = dict()
    for key, value_list in flip_dict(mapping).items():
        if len(value_list) == 1:
            inversion[key] = safe_strip(value_list[0])
        else:
            for idx, _ in enumerate(value_list):
                new_key = str(key) + _SEPARATOR + str(idx + 1)
                inversion[new_key] = safe_strip(value_list[idx])
    return dict(inversion)


def flip_dict(mapping: dict) -> dict:
    """Flip a Python :class:`dict` by collecting duplicate values in a list."""
    flipped = {}
    for key, value in mapping.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)
    return flipped


def _strip_index(string: str) -> str:
    """Strip any potential indices of a `string`."""
    if not isinstance(string, str):
        return string
    if _SEPARATOR not in string:
        return string
    components = string.split(_SEPARATOR)
    if not components[-1].isdigit():
        return string
    return _SEPARATOR.join(components[:-1])


def _cast_string(string: str):
    """Cast a `str` to `int`, `float`, etc."""
    if not isinstance(string, str):
        return string
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            try:
                return complex(string)
            except ValueError:
                return string


def _id_to_name(model):
    """Extract final state ID to particle name mapping.

    Parameters:
        model: can be either a `str` with the XML model filename or a
        `.Kinematics` object directly.
    """
    if isinstance(model, str):
        return pwa.get_final_state_id_to_name_mapping(model)
    if isinstance(model, pwa.Kinematics):
        trans = model.get_particle_state_transition_kinematics_info()
        return trans.get_final_state_id_to_name_mapping()
    raise exception.MissingParameter(
        "Parameter model needs to be either a str or a Kinematics instance"
    )
