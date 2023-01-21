import numpy as np

from stitch_generator.collection.functions.functions_1d import linear_0_1
from stitch_generator.collection.motifs.collection import zigzag_rectangle
from stitch_generator.collection.motifs.square_spiral import square_spiral
from stitch_generator.collection.subdivision.tatami import tatami_3_1, tatami
from stitch_generator.framework.path import get_inset_path
from stitch_generator.functions.function_modifiers import chain
from stitch_generator.functions.functions_1d import square
from stitch_generator.subdivision.subdivide_by_length import regular
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.subdivision.subdivide_by_pattern import pattern_from_spaces, subdivision_by_pattern
from stitch_generator.subdivision.subdivision_modifiers import alternate_direction, add_end, add_start
from stitch_generator.shapes.line import line_shape
from stitch_generator.stitch_effects.path_effects.contour import contour
from stitch_generator.stitch_effects.path_effects.lattice import lattice
from stitch_generator.stitch_effects.path_effects.meander import meander
from stitch_generator.stitch_effects.path_effects.satin import satin
from stitch_generator.stitch_effects.path_effects.scribble import scribble
from stitch_generator.stitch_effects.path_effects.stripes import stripes, parallel_stripes
from stitch_generator.stitch_effects.path_effects.tile_motif import tile_motif
from stitch_generator.stitch_effects.path_effects.variable_underlay import variable_underlay
from stitch_generator.stitch_effects.path_effects.zigzag import zigzag, double_zigzag
from stitch_generator.stitch_operations.remove_duplicates import remove_duplicates


def stitch_effect_collection():
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
    effect = meander(spacing_function=regular(3), line_subdivision=regular(3))
    return effect(path)


def stitch_effect_meander_join_ends(path):
    effect = meander(spacing_function=regular(2),
                     line_subdivision=regular(3),
                     join_ends=True)
    return effect(path)


def stitch_effect_meander_pattern(path):
    line_subdivision = alternate_direction(add_start(add_end(tatami_3_1(segment_length=3))))
    effect = meander(spacing_function=regular(2), line_subdivision=line_subdivision, join_ends=False)
    return effect(path)


def stitch_effect_meander_spacing_pattern(path):
    effect = meander(spacing_function=subdivision_by_pattern(pattern=(0, 0.7), pattern_length=5, alignment=0, offset=0),
                     line_subdivision=regular(3))
    return effect(path)


def stitch_effect_satin(path):
    line_subdivision = add_start(alternate_direction(
        tatami(segment_length=3, steps=5, repetitions=1, minimal_segment_size=2)))
    effect = satin(spacing_function=regular(2),
                   line_subdivision=line_subdivision)
    return effect(path)


def stitch_effect_scribble(path):
    line_subdivision = alternate_direction(add_start(add_end(tatami_3_1(segment_length=3))))
    effect = scribble(repetitions=4, line_subdivision=line_subdivision, noise_scale=0.25)
    return effect(path)


def stitch_effect_scribble_dense(path):
    line_subdivision = alternate_direction(tatami_3_1(segment_length=3))
    effect = scribble(repetitions=10, line_subdivision=line_subdivision)
    return effect(path)


def stitch_effect_stripes(path):
    effect = stripes(steps=subdivide_by_number(6), line_subdivision=regular(3))
    return effect(path)


def stitch_effect_parallel_stripes(path):
    effect = parallel_stripes(steps=subdivide_by_number(3), line_subdivision=regular(3))
    return effect(path)


def stitch_effect_parallel_stripes_pattern(path):
    effect = parallel_stripes(steps=pattern_from_spaces((1, 2, 1, 2, 1), with_start=True, with_end=True),
                              line_subdivision=regular(3))
    return effect(path)


def stitch_effect_tile_motif_spiral(path):
    # create motif for tiling
    spiral_level = 5
    motif_scale = (1, spiral_level / (spiral_level - 1))  # make it square
    motif_translation = (0.5, 0.5)  # move it into the range [0,1] in x and y direction
    motif = square_spiral(level=spiral_level, step_size=(1 / spiral_level)) * motif_scale + motif_translation

    # create stitch effect
    effect = chain(tile_motif(motif=motif, motif_length=15), remove_duplicates)
    return effect(path)


def stitch_effect_tile_motif_zigzag(path):
    # create motif for tiling
    motif_translation = (0.5, 0.5)  # move it into the range [0,1] in x and y direction
    motif = zigzag_rectangle(width=1, height=1, repetitions=8, horizontal=False) + motif_translation
    motif = np.concatenate((line_shape((0, 1), (1, 0))(subdivide_by_number(4)[:-1]), motif))

    # create stitch effect
    effect = chain(tile_motif(motif=motif, motif_length=5), remove_duplicates)
    return effect(path)


def stitch_effect_variable_underlay(path):
    path = get_inset_path(path, inset=1)
    effect = variable_underlay(stroke_spacing=3, line_subdivision=regular(3))
    return effect(path)


def stitch_effect_zigzag(path):
    effect = zigzag(spacing_function=regular(3))
    return effect(path)


def stitch_effect_double_zigzag(path):
    effect = double_zigzag(spacing_function=regular(3))
    return effect(path)
