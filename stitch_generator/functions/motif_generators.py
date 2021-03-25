import itertools

import numpy as np


def repeat_motif(motif):
    return itertools.repeat(motif)


def cycle_motifs(motifs):
    return itertools.cycle(motifs)


def repeat_motif_mirrored(motif):
    mirrored = motif.copy() * np.array((-1, 1))
    while True:
        yield motif
        yield mirrored


def alternate_direction(motif_generator):
    direction = itertools.cycle(((1, 1), (-1, 1)))
    while True:
        yield next(motif_generator) * next(direction)


def combine_motif_mirrored(motif):
    mirrored = motif.copy() * np.array((-1, 1))
    combined = np.concatenate((motif, mirrored[1:]))
    return combined
