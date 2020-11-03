import itertools

import numpy as np


def repeat_motif(motif):
    return itertools.repeat(motif)


def cycle_motifs(motifs):
    return itertools.cycle(motifs)


def repeat_motif_mirrored(motif):
    mirrored = motif.copy() * np.array((-1, 1))
    while (True):
        yield motif
        yield mirrored


def combine_motif_mirrored(motif):
    mirrored = motif.copy() * np.array((-1, 1))
    combined = np.concatenate((motif, mirrored[1:]))
    return combined