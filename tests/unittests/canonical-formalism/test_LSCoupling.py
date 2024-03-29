import pytest

from pycompwa.expertsystem.state.conservationrules import (
    ParityConservationHelicity,
)
from pycompwa.expertsystem.state.particle import (
    InteractionQuantumNumberNames,
    Spin,
    SpinQNConverter,
    XMLLabelConstants,
)
from pycompwa.expertsystem.ui.default_settings import (
    create_default_interaction_settings,
)
from pycompwa.expertsystem.ui.system_control import (
    InteractionTypes,
    StateTransitionManager,
    remove_conservation_law,
)


@pytest.mark.parametrize(
    "initial_state,final_state,L,S,solution_count",
    [
        (
            [("Y", [1])],
            [("D*(2007)0bar", [0]), ("D*(2007)0", [0])],
            Spin(1, 0),
            Spin(0, 0),
            1,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [1]), ("D*(2007)0", [0])],
            Spin(1, 0),
            Spin(0, 0),
            0,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [1]), ("D*(2007)0", [0])],
            Spin(1, 0),
            Spin(1, 0),
            1,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [0]), ("D*(2007)0", [0])],
            Spin(1, 0),
            Spin(1, 0),
            0,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [1]), ("D*(2007)0", [0])],
            Spin(1, 0),
            Spin(2, 0),
            1,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [0]), ("D*(2007)0", [0])],
            Spin(1, 0),
            Spin(2, 0),
            1,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [0]), ("D*(2007)0", [1])],
            Spin(1, 0),
            Spin(0, 0),
            0,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [0]), ("D*(2007)0", [1])],
            Spin(1, 0),
            Spin(1, 0),
            1,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [0]), ("D*(2007)0", [1])],
            Spin(1, 0),
            Spin(2, 0),
            1,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [0]), ("D*(2007)0", [-1])],
            Spin(1, 0),
            Spin(0, 0),
            0,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [0]), ("D*(2007)0", [-1])],
            Spin(1, 0),
            Spin(1, 0),
            1,
        ),
        (
            [("Y", [1])],
            [("D*(2007)0bar", [0]), ("D*(2007)0", [-1])],
            Spin(1, 0),
            Spin(2, 0),
            1,
        ),
    ],
)
def test_canonical_clebsch_gordan_ls_coupling(
    initial_state, final_state, L, S, solution_count
):
    # because the amount of solutions is too big we change the default domains
    formalism_type = "canonical-helicity"
    int_settings = create_default_interaction_settings(formalism_type)

    remove_conservation_law(
        int_settings[InteractionTypes.Strong], ParityConservationHelicity()
    )

    tbd_manager = StateTransitionManager(
        initial_state,
        final_state,
        [],
        interaction_type_settings=int_settings,
        formalism_type=formalism_type,
    )

    tbd_manager.set_allowed_interaction_types([InteractionTypes.Strong])
    tbd_manager.number_of_threads = 2
    tbd_manager.filter_remove_qns = []

    l_label = InteractionQuantumNumberNames.L
    s_label = InteractionQuantumNumberNames.S
    qn_label = XMLLabelConstants.QuantumNumber

    spin_converter = SpinQNConverter()
    node_props = {
        0: {
            qn_label.name: [
                spin_converter.convert_to_dict(l_label, L),
                spin_converter.convert_to_dict(s_label, S),
            ]
        }
    }
    graph_node_setting_pairs = tbd_manager.prepare_graphs()
    for v in graph_node_setting_pairs.values():
        for e in v:
            e[0].node_props = node_props

    solutions = tbd_manager.find_solutions(graph_node_setting_pairs)[0]

    assert len(solutions) == solution_count
