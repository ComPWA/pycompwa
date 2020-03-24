"""A façade to the :class:`~.HelicityKinematics` class.

.. todo:
    These functions are basically façades to the :mod:`pycompwa.ui` so don't
    belong in the :mod:`pycompwa.data` module.
"""


__all__ = [
    'compute',
    'id_to_name_map',
    'load',
]


import pycompwa.ui as pwa


def compute(events: pwa.EventCollection, model: str) -> pwa.DataSet:
    """Compute kinematic variables for each event."""
    kinematics = load(model)
    kinematics.create_all_subsystems()
    return kinematics.convert(events)


def id_to_name_map(model) -> dict:
    """Extract final state ID to particle name mapping."""
    kinematics = load(model)
    trans = kinematics.get_particle_state_transition_kinematics_info()
    return trans.get_final_state_id_to_name_mapping()


def load(model: str) -> pwa.HelicityKinematics:
    """Create a :class:`~.HelicityKinematics` object.

    Parameters:
        model: filename of an XML model file or `.Kinematics` object directly.
    """
    if isinstance(model, str):
        particle_list = pwa.read_particles(model)
        return pwa.create_helicity_kinematics(model, particle_list)
    if isinstance(model, pwa.Kinematics):
        return model
    raise TypeError('model should be either file name or an XML filename')
