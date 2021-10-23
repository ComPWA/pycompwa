# cspell:ignore astype dropna Fourvecs
"""Import Pawian data files.

For more information, see the `Pawian website
<https://panda-wiki.gsi.de/foswiki/bin/view/PWA/PawianPwaSoftware>`_.
The functions in this module contain several logical statements for backward
compatibility to ASCII files without header.
"""


__all__ = [
    "read_ascii",
    "read_hists_file",
    "write_ascii",
]


import pandas as pd
import uproot3

import pycompwa.ui as pwa
from pycompwa.data import _labels, convert, create, exception


def read_hists_file(filename: str, type_name: str = "data"):
    r"""
    Import one of the momentum tuple branches of a ``pawianHists.root`` file.

    .. note::
        There are slight differences in ROOT files that were written with ROOT5
        versus those from ROOT6, but this function takes care of that.

    Parameters:
        filename (`str`): path to the ROOT file you want to import.
        type_name (`str`, optional): \"data\" or \"fit\".
    """
    # Determine tree name
    if "dat" in type_name.lower():
        type_name = "data"
    elif "fit" in type_name.lower():
        type_name = "fitted"
    else:
        raise exception.MissingParameter(
            f'Wrong type_name: should be either "data" or "fit"'
        )
    tree_name = f"_{type_name}Fourvecs"

    # Get particle names
    uproot_file = uproot3.open(filename)
    tree = uproot_file[tree_name]
    particles = [
        particle.decode()
        for particle in tree.keys()
        if particle.decode() != _labels.WEIGHT
    ]

    # Import tuples as dataframe
    weights = uproot_file[f"{tree_name}/{_labels.WEIGHT}"].array()
    frame = create.pwa_frame(
        particle_names=particles,
        number_of_rows=len(weights),
    )
    if weights.max() != 1.0 and weights.min() != 1.0:
        frame[_labels.WEIGHT] = weights
    try:  # ROOT >= 6
        for particle in particles:
            vectors = uproot_file[f"{tree_name}/{particle}"].array()
            frame[particle, _labels.MOMENTA[0]] = vectors.x
            frame[particle, _labels.MOMENTA[1]] = vectors.y
            frame[particle, _labels.MOMENTA[2]] = vectors.z
            frame[particle, _labels.MOMENTA[3]] = vectors.E
    except ValueError:  # ROOT <= 5
        for particle in particles:
            particle_branch = f"{tree_name}/{particle}"
            frame[particle, _labels.MOMENTA[0]] = uproot_file[
                f"{particle_branch}/fP/fP.fX"
            ].array()
            frame[particle, _labels.MOMENTA[1]] = uproot_file[
                f"{particle_branch}/fP/fP.fY"
            ].array()
            frame[particle, _labels.MOMENTA[2]] = uproot_file[
                f"{particle_branch}/fP/fP.fZ"
            ].array()
            frame[particle, _labels.ENERGY] = uproot_file[
                f"{particle_branch}/fE"
            ].array()
    return frame


def read_ascii(filename, particles=None, **kwargs):
    """Import from a Pawian-like ASCII file.

    Parameters:
        particles: Interpretation for the tuples. This argument is required if
            there are no weights. Provide either the number of particles or a
            list of particles.
        kwargs: Optional, additional arguments that are passed on to
            `pandas.read_table`.
    """
    try:
        frame = _read_ascii_with_header(filename, particles)
    except RuntimeError:  # exception raised by pycompwa.ui.read_ascii_data
        frame = _read_ascii_without_header(filename, particles, **kwargs)
    return frame


def _read_ascii_with_header(filename, particles=None):
    """Import ASCII file **with** header."""
    event_collection = pwa.read_ascii_data(filename)
    frame = convert.events_to_pandas(event_collection)
    particles_in_frame = frame.pwa.particles
    if isinstance(particles, list) and len(particles_in_frame) != len(
        particles
    ):
        raise exception.DataException(
            f"The number of particles in argument particles ({particles}) "
            "does not have the same number of particles as inferred from "
            f"the ASCII header of file ({particles_in_frame})"
        )
    return frame


def _read_ascii_without_header(filename, particles=None, **kwargs):
    """Import ASCII file **without header** (old Pawian format)."""
    full_table = pd.read_table(
        filepath_or_buffer=filename,
        names=_labels.MOMENTA,
        sep=R"\s+",
        skip_blank_lines=True,
        dtype="float64",
        **kwargs,
    )

    # Determine if ascii file contains weights
    py_values = full_table[_labels.MOMENTA[1]]
    has_weights = py_values.isnull().any()
    if not has_weights:
        if isinstance(particles, int):
            particles = range(1, particles + 1)
        elif particles is None or not isinstance(particles, list):
            raise exception.DataException(
                "Cannot determine number of particles in file"
                f'"{filename}"\n'
                "--> Please provide an array of particles for"
                "interpretation"
            )

    # Try to determine number of particles from file
    if has_weights:
        file_n_partices = py_values.index[py_values.isnull()][1] - 1
        if particles is None:
            particles = range(1, file_n_partices + 1)
        if isinstance(particles, int):
            particles = range(1, particles + 1)
        if len(particles) != file_n_partices:
            raise exception.DataException(
                f'File "{filename}" contains {file_n_partices}, but you'
                f"said there were {len(particles)} ({particles})"
            )

    # Prepare splitting into particle columns
    first_momentum_row = 0
    n_rows = len(particles)
    if has_weights:
        first_momentum_row = 1
        n_rows += 1

    # Create multi-column pandas.DataFrame
    frame = create.pwa_frame(
        particle_names=particles,
        number_of_rows=len(full_table) // n_rows,
    )
    particles = frame.pwa.particles

    # Convert imported table to the multi-column one
    if has_weights:
        frame[_labels.WEIGHT] = full_table[_labels.MOMENTA[0]][
            0::n_rows
        ].reset_index(drop=True)
    for start_row, par in enumerate(particles, first_momentum_row):
        for mom in _labels.MOMENTA:
            frame[par, mom] = full_table[mom][start_row::n_rows].reset_index(
                drop=True
            )
    return frame


def write_ascii(frame: pd.DataFrame, filename: str, **kwargs):
    """Write :class:`pandas.DataFrame` to a Pawian-like ASCII file.

    Parameters:
        frame (:class:`pandas.DataFrame`): The frame that you want to export.
            Should be formatted according to the standards set by the
            :class:`~.PwaAccessor`.
        filename (`str`): Path of the output file. Usually has the extension
            ``dat``.
        kwargs: Optional, additional arguments that are passed on to
            :meth:`pandas.DataFrame.to_csv`.
    """
    new_dict = list()
    if frame.pwa.weights is not None:
        new_dict.append(frame.pwa.weights)
    for par in frame.pwa.particles:
        new_dict.append(
            frame[par].apply(
                lambda x: " ".join(x.dropna().astype(str)),
                axis=1,
            )
        )
    interleaved = pd.concat(new_dict).sort_index(kind="mergesort")
    interleaved.to_csv(filename, header=False, index=False, **kwargs)
