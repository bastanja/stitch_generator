import itertools
from functools import partial

import numpy as np

from stitch_generator.functions.functions_2d import line
from stitch_generator.functions.samples import samples_by_fixed_length_with_alignment, samples_by_length


def line_constant_stitch_length(stitch_length):
    return partial(_line_constant_stitch_length, stitch_length=stitch_length)


def line_fixed_stitch_length(stitch_length, alignment):
    return partial(_line_fixed_stitch_length(stitch_length=stitch_length, alignment=alignment))


def alternate_direction(stitch_length, alignment):
    forward = itertools.cycle((True, False))

    def f(p1, p2):
        length = np.linalg.norm(p2 - p1)
        p = line(p1, p2)
        alignment_to_use = alignment if next(forward) else 1 - alignment
        return p(samples_by_fixed_length_with_alignment(length, stitch_length, alignment_to_use))

    return f


def combine_start_end(connect_function):
    last_point = None

    def f(p1, p2):
        points = connect_function(p1, p2)

        nonlocal last_point
        try:
            points[0] = (points[0] + last_point) / 2
        except TypeError:
            # if last_point was not set yet, ignore it
            pass

        last_point = points[-1]
        return points[0: -1]

    return f


def _line_constant_stitch_length(p1, p2, stitch_length):
    length = np.linalg.norm(p2 - p1)
    t = samples_by_length(length, stitch_length, include_endpoint=True)
    return line(p1, p2)(t)


def _line_fixed_stitch_length(p1, p2, stitch_length, alignment):
    length = np.linalg.norm(p2 - p1)
    t = samples_by_fixed_length_with_alignment(length, stitch_length, alignment)
    return line(p1, p2)(t)
