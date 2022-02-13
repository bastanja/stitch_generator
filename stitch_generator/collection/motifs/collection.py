import numpy as np

from stitch_generator.functions.ensure_shape import ensure_2d_shape
from stitch_generator.sampling.sample_by_number import sampling_by_number
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.path_effects.zigzag import zigzag_between


def zigzag(width: float, height: float, repetitions: int, flip: bool = False):
    half_width = width / 2
    half_height = height / 2

    if flip:
        half_height = -half_height

    f1 = line((-half_width, -half_height), (half_width, -half_height))
    f2 = line((-half_width, half_height), (half_width, half_height))

    return zigzag_between(f1, f2, sampling_by_number(repetitions), width)


def zigzag_motif(width: float, height: float, repetitions: int):
    half_width = width / 2

    f1 = line((0, -half_width), (0, half_width))
    f2 = line((height, -half_width), (height, half_width))

    return zigzag_between(f1, f2, sampling_by_number(repetitions), width)


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
    motif = zigzag(width=0.1, height=length, repetitions=repetitions)
    origin = ensure_2d_shape((0, 0))
    return np.concatenate((origin, motif, origin))


def overlock_stitch_motif(width, height):
    stem_height = height / 3
    loop_height = height - stem_height

    return [(-stem_height, 0), (loop_height, 0), (loop_height, width), (0, width / 10), (-stem_height, 0)]
