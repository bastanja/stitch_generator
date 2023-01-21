import numpy as np

from stitch_generator.functions.ensure_shape import ensure_2d_shape
from stitch_generator.subdivision.subdivide_by_number import subdivision_by_number
from stitch_generator.subdivision.subdivision_modifiers import remove_end
from stitch_generator.shapes.circle import circle_shape
from stitch_generator.shapes.line import line_shape
from stitch_generator.stitch_effects.path_effects.zigzag import zigzag_between
from stitch_generator.stitch_operations.rotate import rotate_90


def zigzag_rectangle(width: float, height: float, repetitions: int, horizontal: bool, flip: bool = False):
    if horizontal:
        return _zigzag_rectangle(width=width, height=height, repetitions=repetitions, flip=flip)
    else:
        return rotate_90(_zigzag_rectangle(width=height, height=width, repetitions=repetitions, flip=flip))


def _zigzag_rectangle(width: float, height: float, repetitions: int, flip: bool = False):
    half_width = width / 2
    half_height = height / 2

    if flip:
        half_height = -half_height

    f1 = line_shape((-half_width, -half_height), (half_width, -half_height))
    f2 = line_shape((-half_width, half_height), (half_width, half_height))

    return zigzag_between(f1, f2, subdivision_by_number(repetitions), width)


def zigzag_motif(width: float, height: float, repetitions: int):
    half_width = width / 2

    f1 = line_shape((0, -half_width), (0, half_width))
    f2 = line_shape((height, -half_width), (height, half_width))

    return zigzag_between(f1, f2, subdivision_by_number(repetitions), width)


def rhomb_motif(width, height):
    half_width = width / 2
    half_height = height / 2
    return np.array(((-half_height, 0), (0, -half_width), (half_height, 0), (0, half_width), (-half_height, 0)))


def x_motif(width, height):
    half_width = width / 2
    half_height = height / 2
    motif = np.array(((0, 0), (-half_height, -half_width)))
    return np.concatenate((motif, motif * (1, -1), motif * (-1, -1), motif * (-1, 1), ensure_2d_shape((0, 0))))


def line_motif(length: float, repetitions: int):
    motif = zigzag_rectangle(width=0.1, height=length, repetitions=repetitions, horizontal=True)
    origin = ensure_2d_shape((0, 0))
    return np.concatenate((origin, motif, origin))


def overlock_stitch_motif(width: float, height: float, loop_ratio: float):
    stem_height = height * loop_ratio
    return np.array([(0, height), (0, 0), (width, 0), (width / 10, height - stem_height), (0, height)])


def star_motif(num_spikes: int, inner_radius: float, outer_radius: float):
    inner = circle_shape(inner_radius)
    outer = circle_shape(outer_radius)
    result = zigzag_between(outer, inner, spacing_function=remove_end(subdivision_by_number((num_spikes * 2))), length=1)
    return np.vstack((result[-1], result))
