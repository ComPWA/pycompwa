"""A small script that 'pickles' a PWA-formatted pandas.DataFrame."""


import os
from os.path import dirname, realpath

import pycompwa.ui as pwa
from pycompwa.data import convert


SCRIPT_DIR = dirname(realpath(__file__))
os.makedirs(f'{SCRIPT_DIR}/files', exist_ok=True)


def to_pickle(import_file: str):
    """Import a file with pycompwa and convert it to a `~pandas.DataFrame`."""
    events = pwa.read_ascii_data(import_file)
    frame = convert.events_to_pandas(
        events=events,
        model=f'{SCRIPT_DIR}/files/kinematics.xml')
    output_file = import_file.replace('ascii_', 'pwa_frame_', 1)
    output_file = output_file.replace('.dat', '.pkl')
    frame.to_pickle(output_file)


def main():
    """Exectue as script."""
    pwa.Logging('error')
    to_pickle(f'{SCRIPT_DIR}/files/ascii_weights.dat')
    to_pickle(f'{SCRIPT_DIR}/files/ascii_noweights.dat')


if __name__ == "__main__":
    main()
