import itertools


def repeat_motif(motif):
    return itertools.repeat(motif)


def cycle_motifs(motifs):
    return itertools.cycle(motifs)


def repeat_motif_mirrored(motif):
    return mirror_alternating(repeat_motif(motif))


def mirror_alternating(motif_generator):
    direction = itertools.cycle(((1, 1), (-1, 1)))
    while True:
        yield next(motif_generator) * next(direction)
