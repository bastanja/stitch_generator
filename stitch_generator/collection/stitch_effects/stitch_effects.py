import itertools

import numpy as np

from stitch_generator.collection.functions.functions_1d import linear_0_1
from stitch_generator.collection.motifs.collection import zigzag_rectangle
from stitch_generator.collection.motifs.square_spiral import square_spiral
from stitch_generator.collection.sampling.tatami_sampling import tatami_3_1, tatami
from stitch_generator.framework.path import get_inset_path
from stitch_generator.functions.function_modifiers import repeat
from stitch_generator.functions.functions_1d import square, constant, arc
from stitch_generator.functions.motif_generators import repeat_motif_mirrored
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sample_by_pattern import pattern_from_spaces, sampling_by_pattern
from stitch_generator.sampling.sampling_modifiers import alternate_direction, add_end, add_start, free_start, free_end
from stitch_generator.shapes.circle import circle
from stitch_generator.shapes.line import line
from stitch_generator.stitch_effects.path_effects.contour import contour
from stitch_generator.stitch_effects.path_effects.lattice import lattice
from stitch_generator.stitch_effects.path_effects.meander import meander
from stitch_generator.stitch_effects.path_effects.satin import satin
from stitch_generator.stitch_effects.path_effects.scribble import scribble
from stitch_generator.stitch_effects.path_effects.stripes import stripes, parallel_stripes
from stitch_generator.stitch_effects.path_effects.tile_motif import tile_motif
from stitch_generator.stitch_effects.path_effects.variable_underlay import variable_underlay
from stitch_generator.stitch_effects.path_effects.zigzag import zigzag, double_zigzag
from stitch_generator.stitch_effects.shape_effects.motif_chain import motif_chain
from stitch_generator.stitch_effects.shape_effects.motif_to_points import motif_to_points
from stitch_generator.stitch_effects.shape_effects.motif_to_segments import motif_to_segments
from stitch_generator.stitch_effects.shape_effects.running_stitch import running_stitch
from stitch_generator.stitch_effects.shape_effects.variable_running_stitch import variable_running_stitch


def stitch_effect_contour(path):
    effect = contour(stitch_length=3)
    return effect(path)


def stitch_effect_lattice_linear(path):
    effect = lattice(strands=7, pattern_f=linear_0_1, pattern_length=15)
    return effect(path)


def stitch_effect_lattice_peaks(path):
    effect = lattice(strands=3, pattern_f=square, pattern_length=30)
    return effect(path)


def stitch_effect_meander(path):
    effect = meander(spacing_function=regular(3), line_sampling_function=regular(3))
    return effect(path)


def stitch_effect_meander_join_ends(path):
    effect = meander(spacing_function=regular(2),
                     line_sampling_function=regular(3),
                     join_ends=True)
    return effect(path)


def stitch_effect_meander_pattern(path):
    line_sampling_function = alternate_direction(add_start(add_end(tatami_3_1(segment_length=3))))
    effect = meander(spacing_function=regular(2),
                     line_sampling_function=line_sampling_function,
                     join_ends=False)
    return effect(path)


def stitch_effect_meander_spacing_pattern(path):
    effect = meander(spacing_function=sampling_by_pattern(pattern=(0, 0.7), pattern_length=5, alignment=0, offset=0),
                     line_sampling_function=regular(3))
    return effect(path)


def stitch_effect_satin(path):
    line_sampling_function = add_start(alternate_direction(
        tatami(segment_length=3, steps=5, repetitions=1, minimal_segment_size=2)))
    effect = satin(spacing_function=regular(2),
                   line_sampling_function=line_sampling_function)
    return effect(path)


def stitch_effect_scribble(path):
    line_sampling_function = alternate_direction(add_start(add_end(tatami_3_1(segment_length=3))))
    effect = scribble(repetitions=4, sampling_function=line_sampling_function, noise_scale=0.25)
    return effect(path)


def stitch_effect_scribble_dense(path):
    line_sampling_function = alternate_direction(tatami_3_1(segment_length=3))
    effect = scribble(repetitions=10, sampling_function=line_sampling_function)
    return effect(path)


def stitch_effect_stripes(path):
    effect = stripes(steps=sample_by_number(6), sampling_function=regular(3))
    return effect(path)


def stitch_effect_parallel_stripes(path):
    effect = parallel_stripes(steps=sample_by_number(3), sampling_function=regular(3))
    return effect(path)


def stitch_effect_parallel_stripes_pattern(path):
    effect = parallel_stripes(steps=pattern_from_spaces((1, 2, 1, 2, 1), with_start=True, with_end=True),
                              sampling_function=regular(3))
    return effect(path)


def stitch_effect_tile_motif_spiral(path):
    # create motif for tiling
    spiral_level = 5
    motif_scale = (1, spiral_level / (spiral_level - 1))  # make it square
    motif_translation = (0.5, 0.5)  # move it into the range [0,1] in x and y direction
    motif = square_spiral(level=spiral_level, step_size=(1 / spiral_level)) * motif_scale + motif_translation

    # create stitch effect
    effect = tile_motif(motif=motif, motif_length=15)
    return effect(path)


def stitch_effect_tile_motif_zigzag(path):
    # create motif for tiling
    motif_translation = (0.5, 0.5)  # move it into the range [0,1] in x and y direction
    motif = zigzag_rectangle(width=1, height=1, repetitions=8, horizontal=False) + motif_translation
    motif = np.concatenate((line((0, 1), (1, 0))(sample_by_number(4)[:-1]), motif))

    # create stitch effect
    effect = tile_motif(motif=motif, motif_length=5)
    return effect(path)


def stitch_effect_variable_underlay(path):
    path = get_inset_path(path, inset=1)
    effect = variable_underlay(stroke_spacing=3, sampling_function=regular(3))
    return effect(path)


def stitch_effect_zigzag(path):
    effect = zigzag(spacing_function=regular(3))
    return effect(path)


def stitch_effect_double_zigzag(path):
    effect = double_zigzag(spacing_function=regular(3))
    return effect(path)


def stitch_effect_motif_chain_arrows(path):
    arrow = np.array(((-3, -2), (0, 0), (3, -2)))
    motif_generator = repeat_motif_mirrored(arrow)
    effect = motif_chain(motif_position_sampling=regular(3), motif_generator=motif_generator,
                         motif_rotation_degrees=constant(0))
    return effect(path)


def stitch_effect_motif_chain_loops(path):
    length = 7
    half_width = 2
    arrow = np.array(((-1, 0), (length - 3, half_width), (length - 1, 0), (length - 3, -half_width), (-1, 0)))
    motif_generator = repeat_motif_mirrored(arrow)
    effect = motif_chain(motif_position_sampling=regular(5), motif_generator=motif_generator,
                         motif_rotation_degrees=constant(0))
    return effect(path)


def stitch_effect_motif_chain_pattern(path):
    # create line motif
    motif = np.array(((0, 0), (6, 0), (0, 0)))

    # create pattern for line placement
    pattern = pattern_from_spaces((1, 8, 1), with_start=False, with_end=False)
    position_sampling = sampling_by_pattern(pattern=pattern, pattern_length=7, alignment=0.5, offset=0)

    # create stitch effect
    effect = motif_chain(motif_position_sampling=position_sampling, motif_generator=itertools.repeat(motif),
                         motif_rotation_degrees=constant(0))
    return effect(path)


def stitch_effect_motif_to_points(path):
    # create arrow motif
    motif = np.array(((0, 0.0), (3, -3), (0, 0), (-3, -3), (0, 0)))

    # create pattern for arrow placement
    pattern = pattern_from_spaces((6, 1, 1, 6), with_start=False, with_end=False)
    position_sampling = sampling_by_pattern(pattern=pattern, pattern_length=30, alignment=0.5, offset=0)
    position_sampling = free_start(10, free_end(10, position_sampling))

    # create stitch effect
    effect = motif_to_points(motif_position_sampling=position_sampling, line_sampling=regular(3),
                             motif_generator=itertools.repeat(motif))
    return effect(path)


def stitch_effect_motif_to_segments(path):
    motif = repeat(0.5, circle(radius=7))(sample_by_number(8))
    position_sampling = free_start(10, free_end(10, regular(25)))
    effect = motif_to_segments(motif_position_sampling=position_sampling, line_sampling=regular(3),
                               motif_generator=itertools.repeat(motif), motif_length=14)
    return effect(path)


def stitch_effect_running_stitch(path):
    effect = running_stitch(stitch_length=3)
    return effect(path)


def stitch_effect_variable_running_stitch(path):
    effect = variable_running_stitch(stitch_length=3, width_profile=arc, min_strokes=1, max_strokes=7,
                                     stroke_spacing=0.3)
    return effect(path)


def path_effects():
    yield stitch_effect_contour
    yield stitch_effect_lattice_linear
    yield stitch_effect_lattice_peaks
    yield stitch_effect_meander
    yield stitch_effect_meander_join_ends
    yield stitch_effect_meander_pattern
    yield stitch_effect_meander_spacing_pattern
    yield stitch_effect_satin
    yield stitch_effect_scribble
    yield stitch_effect_scribble_dense
    yield stitch_effect_stripes
    yield stitch_effect_parallel_stripes
    yield stitch_effect_parallel_stripes_pattern
    yield stitch_effect_tile_motif_spiral
    yield stitch_effect_tile_motif_zigzag
    yield stitch_effect_variable_underlay
    yield stitch_effect_zigzag
    yield stitch_effect_double_zigzag


def shape_effects():
    yield stitch_effect_motif_chain_arrows
    yield stitch_effect_motif_chain_loops
    yield stitch_effect_motif_chain_pattern
    yield stitch_effect_motif_to_points
    yield stitch_effect_motif_to_segments
    yield stitch_effect_running_stitch
    yield stitch_effect_variable_running_stitch
