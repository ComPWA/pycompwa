"""PWA Expert System.

The goal is to build state transition graphs, going from an initial state to a
final state. A state transition graph consists of nodes and edges/lines (in
correspondence to feynman graphs):

- The connection lines we call particle lines, which are basically a list of
  quantum numbers (QN) that define the particle state (That list can be empty
  at first).

- The nodes are of type InteractionNode, that contain all information for the
  transition of this specific step. An interaction node has M ingoing lines and
  :math:`N` outgoing lines (:math:`M,N \in \mathbb{Z}` and :math:`M>0, N>0`).

The concept of building graphs is as follows:

- **Step 1**: Building of all possible topologies. A topology is a graph, in
  which the edges and nodes are empty (no QN information). See the topology
  sub-modules.

- **Step 2**: Filling the topology graphs with QN information. This means
  initializing the topology graphs with the initial and final state quantum
  numbers and propagating these through the complete graph. Here also the
  combinatorics of the initial and final state should be taken into account.

- **Step 3**: Duplicate the graphs and insert concrete particles for the edges
  (inserting the mass variable)

- **Step 4**: Output to XML model file.

.. seealso:: :doc:`/usage/workflow/step1`
"""

from . import amplitude, state, topology, ui

__all__ = [
    "amplitude",
    "state",
    "topology",
    "ui",
]


if __name__ == "__main__":
    import sys

    def print_message_and_exit():
        print(
            "You are running python "
            + str(sys.version_info[0])
            + "."
            + str(sys.version_info[1])
            + "."
            + str(sys.version_info[2])
        )
        print("The ComPWA expertsystem required python 3.3 or higher!")
        sys.exit()

    if sys.version_info.major < 3:
        print_message_and_exit()
    elif sys.version_info.major == 3 and sys.version_info.minor < 3:
        print_message_and_exit()
