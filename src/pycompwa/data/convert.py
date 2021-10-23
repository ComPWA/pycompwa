# cspell:ignore pids
"""Conversion tools between from ComPWA objects and :class:`pandas.DataFrame`.

This module contains functions that help convertion from ComPWA objects like
:class:`~.EventCollection` and :class:`~.DataSet` to a
:class:`~pandas.DataFrame` and back.
"""


__all__ = [
    "data_set_to_pandas",
    "events_to_pandas",
    "pandas_to_events",
]


import pandas as pd

import pycompwa.ui as pwa

from . import _labels, create, exception, naming


def events_to_pandas(
    events: pwa.EventCollection, model: str = None
) -> pd.DataFrame:
    """Convert an `~.EventCollection` to a  `~pandas.DataFrame`.

    Create a PWA formatted `~pandas.DataFrame` from an
    `~.EventCollection`.

    Parameters:
        events: The `~.EventCollection` that you want to convert.
        model: Name of the XML file containing the kinematic info or a
            `.Kinematics` instance. **Required if you want to rename the
            PIDs!**
    Raises:
        ConfigurationConflict: Number of final state particles in XML does not
            agree with number of final state particles in `~.PwaAccessor`.
    """
    pids = events.pids
    if model:
        id_to_name = pwa.get_final_state_id_to_name_mapping(model)
        if len(id_to_name) != len(pids):
            raise exception.ConfigurationConflict(
                f"XML file {model} has {len(id_to_name)} final state"
                f"particles, the event collection has {len(pids)}"
            )
        particle_list = pwa.read_particles(model)
        pids = [
            particle_list.name_to_pid(name) for name in id_to_name.values()
        ]
    particles = naming.make_values_unique(pids)
    frame = create.pwa_frame(events.to_table(), particle_names=particles)
    if model:
        particle_list = pwa.read_particles(model)
        naming.pid_to_name(frame, particle_list)
    if events.has_weights():
        frame[_labels.WEIGHT] = events.weights()
    return frame


def pandas_to_events(frame: pd.DataFrame, model: str) -> pwa.EventCollection:
    """Convert :class:`~pandas.DataFrame` to an :class:`~.EventCollection`.

    Create a :class:`PWA formatted DataFrame <.PwaAccessor>` from an
    :class:`~.EventCollection` object.
    """
    particle_list = pwa.read_particles(model)
    id_to_name = pwa.get_final_state_id_to_name_mapping(model)
    ids = list(id_to_name.keys())
    pids = [particle_list.name_to_pid(name) for name in id_to_name.values()]
    if not set(ids) <= set(frame.pwa.particles):
        raise exception.DataException(
            "\n  You first have to convert the columns names:\n"
            f"    {frame.pwa.particles}\n"
            "  to the final state IDs:\n"
            f"    {ids}\n"
            "  as defined in XML file\n"
            f'    "{model}"\n'
            "  with e.g. naming.particle_to_id or pandas.DataFrame.rename"
        )
    numpy_arrays = [
        frame[particle].to_numpy() for particle in frame.pwa.particles
    ]
    if frame.pwa.has_weights:
        events = [
            pwa.Event(
                pwa.FourMomentumList(
                    [pwa.FourMomentum(momentum) for momentum in event[:-1]]
                ),
                event[-1],
            )
            for event in zip(*numpy_arrays, frame.pwa.weights)
        ]
    else:  # default constructor if no weights
        events = [
            pwa.Event(
                pwa.FourMomentumList(
                    [pwa.FourMomentum(momentum) for momentum in event]
                )
            )
            for event in zip(*numpy_arrays)
        ]
    return pwa.EventCollection(pids, pwa.EventList(events))


def data_set_to_pandas(data_set: pwa.DataSet) -> pd.DataFrame:
    """Convert :class:`~.DataSet` to a :class:`~pandas.DataFrame`.

    Convert a :class:`~.DataSet` to a :class:`~pandas.DataFrame`.
    """
    frame = pd.DataFrame(data_set.data, columns=data_set.data.keys())
    if data_set.has_weights():
        frame[_labels.WEIGHT] = data_set.weights
    return frame
