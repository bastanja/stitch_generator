import numpy as np

from stitch_generator.functions.function_modifiers import mix, rotate_degrees
from stitch_generator.functions.functions_1d import constant, arc, linear_interpolation
from stitch_generator.functions.functions_2d import constant_direction
from stitch_generator.functions.motif_generators import cycle_motifs
from stitch_generator.framework.path import Path
from stitch_generator.sampling.sample_by_number import sample_by_number, sampling_by_number
from stitch_generator.utilities.types import Function1D
from stitch_generator.motifs.line import bent_line_with_motif
from stitch_generator.stitch_effects.motif_to_points import motif_to_points


def bundle(start_angle, end_angle, bend_angle_start, bend_angle_end, min_length, max_length, number_of_lines,
           stitch_length, motif_generator):
    length = mix(constant(min_length), constant(max_length), arc)
    bend = mix(constant(bend_angle_start), constant(bend_angle_end), linear_interpolation(0, 1))
    angle = linear_interpolation(start_angle, end_angle)

    return bundle_f(angle, bend, length, number_of_lines, stitch_length, motif_generator)


def bundle_f(angle: Function1D, bend: Function1D, length: Function1D, number_of_lines, stitch_length, motif_generator):
    gen = _motif_generator(number_of_lines-1, stitch_length, bend, length, motif_generator)

    stitch_effect = motif_to_points(sampling_by_number(number_of_lines-1, include_endpoint=True),
                                    line_sampling=lambda _: np.array([]),
                                    motif_generator=gen)

    return np.vstack((stitch_effect(_zero_path(angle)), [0, 0]))


def _motif_generator(number, stitch_length, bend_f, length_f, motif):
    samples = sample_by_number(number, include_endpoint=True)
    lengths = length_f(samples)
    angles = bend_f(samples)
    motifs = [bent_line_with_motif(length, stitch_length, angle, next(motif)) for length, angle in zip(lengths, angles)]
    return cycle_motifs(motifs)


def _zero_path(angle_f: Function1D):
    return Path(shape=constant_direction(0, 0),
                direction=rotate_degrees(constant_direction(1, 0), angle_f),
                width=constant(1),
                stroke_alignment=constant(0.5))
