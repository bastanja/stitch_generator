import numpy as np

from stitch_generator.collection.motifs.collection import zigzag_rectangle, zigzag_motif, rhomb_motif, x_motif, \
    line_motif, overlock_stitch_motif
from stitch_generator.framework.path import Path, get_boundaries
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.functions.function_modifiers import mix, inverse
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.motif_generators import repeat_motif, repeat_motif_mirrored
from stitch_generator.shapes.line import line_shape
from stitch_generator.stitch_effects.path_effects.tile_motif import tile_motif
from stitch_generator.stitch_effects.shape_effects.motif_chain import motif_chain
from stitch_generator.stitch_effects.shape_effects.motif_to_points import motif_to_points
from stitch_generator.stitch_effects.shape_effects.motif_to_segments import motif_to_segments
from stitch_generator.stitch_operations.repeat_stitches import repeat_stitches
from stitch_generator.stitch_operations.rotate import rotate_by_degrees, rotate_270
from stitch_generator.subdivision.subdivide_by_length import subdivision_by_length, subdivision_by_length_with_offset, \
    regular, subdivide_by_length
from stitch_generator.subdivision.subdivision_modifiers import remove_end, add_end, add_start, free_end, free_start


def decorative_stitches_collection(spacing: float = 2.5, stitch_width: float = 5, pattern_spacing: float = 20):
    yield alternating_triangles(spacing=spacing, line_length=4, width=stitch_width, repetitions=3)
    yield arrow_chain(arrow_width=stitch_width, arrow_length=2, arrow_spacing=spacing)
    yield chevron_stitch(spacing=spacing * 2, line_length=3, width=stitch_width, repetitions=5)
    yield cretan_stitch(spacing=spacing * 2, stitch_width=0.1, stitch_length=3, repetitions=4, zigzag_width=2)
    yield cretan_stitch(spacing=spacing * 2, stitch_width=0.1, stitch_length=3.5, repetitions=4)
    yield e_stitch(spacing=spacing, line_length=4, stitch_length=10, angle=45)
    yield feather_stitch(spacing=spacing, stitch_width=0, stitch_length=3.5, repetitions=2)
    yield overlock_stitch(length=spacing, width=stitch_width)
    yield rhomb_motif_stitch(spacing=spacing, width=stitch_width, length=4)
    yield stem_stitch(spacing=spacing, stitch_width=0.6, stitch_length=5, repetitions=5, angle=-25)
    yield stem_stitch(spacing=spacing, stitch_width=stitch_width, stitch_length=4, repetitions=5, angle=0)
    yield three_arrows(arrow_spacing=2, group_spacing=pattern_spacing, start_end_spacing=pattern_spacing / 2,
                       stitch_length=3)
    yield x_motif_stitch(spacing=spacing, width=stitch_width, length=4)


def alternating_triangles(spacing: float, line_length: float, width: float, repetitions: int):
    """
    Returns a stitch effect that creates a thick outline with a zigzag pattern in between.

    Args:
        spacing: The spacing between the middle points of the outline stitches
        line_length: The length of the outline stitches. Should be smaller than spacing to avoid overlaps.
        width: The total width of the resulting stitch pattern
        repetitions: How often an outline stitch is repeated to form a thick line
    """
    motif = zigzag_rectangle(width=0.1, height=-line_length, repetitions=repetitions, horizontal=True, flip=True)
    motif += (width / 2, 0)
    motif_gen = repeat_motif_mirrored(motif)
    subdivision = subdivision_by_length(spacing)
    return motif_chain(subdivision, motif_gen, constant(0))


def arrow_chain(arrow_width: float, arrow_length: float, arrow_spacing: float) -> StitchEffect:
    """
    Returns a stitch effect which places arrows along the path.

    Args:
        arrow_width: The total width of the resulting stitch pattern
        arrow_length: The length of a single arrow
        arrow_spacing: The spacing between two arrows
    """
    single_arrow = np.array(((-arrow_width / 2, -arrow_length), (0, 0), (arrow_width / 2, -arrow_length)))
    motif_gen = repeat_motif_mirrored(single_arrow)
    subdivision = subdivision_by_length(arrow_spacing)
    return motif_chain(subdivision, motif_gen, constant(0))


def chevron_stitch(spacing: float, line_length: float, repetitions: int, width: float):
    """
    Returns a stitch effect that creates a zigzag line with small lines pointing in the direction of the path at each
    spike. Resembles a hand embroidered chevron stitch.

    Args:
        spacing: The spacing between two spikes at the same side of the path
        line_length: The length of the outline stitches. Should be smaller than spacing to avoid overlaps.
        repetitions: How often an outline stitch is repeated to form a thick line
        width: The total width of the resulting stitch pattern
    """
    motif = line_motif(line_length, repetitions) + (width / 2, 0)
    motif_gen = repeat_motif_mirrored(motif)
    subdivision = subdivision_by_length(spacing / 2)
    return motif_chain(subdivision, motif_gen, constant(0))


def cretan_stitch(spacing: float, stitch_width: float, stitch_length: float, repetitions: int,
                  zigzag_width: float = 0):
    """
    Returns a stitch effect that creates a zigzag line with small lines pointing to the side of the path at each spike.

    Args:
        spacing: The spacing between two spikes at the same side of the path
        stitch_width: The width of a line pointing to the side. Should be small, e.g. 0.5
        stitch_length: The length of a line pointing to the side.
        repetitions: How often a line pointing to the side is repeated.
        zigzag_width: The width of the middle zigzag line
    """
    motif = zigzag_motif(stitch_width, stitch_length, repetitions) + (zigzag_width / 2, 0)
    motif_gen = repeat_motif_mirrored(motif)
    subdivision = subdivision_by_length(spacing / 2)
    return motif_chain(subdivision, motif_gen, constant(0))


def e_stitch(spacing: float, line_length: float, stitch_length: float, angle: float) -> StitchEffect:
    """
    Returns a stitch effect that creates a line along the path with small lines pointing to the side, similar to the
    letter 'E'.

    Args:
        spacing: The spacing between the lines pointing to the side
        line_length: The length of  the lines pointing to the side
        stitch_length: The stitch length of the middle line and the lines pointing to the side. Only relevant if
                       stitch_length is smaller than line_length or spacing.
        angle: The rotation angle in degrees by which the small lines are rotated relative to the direction of the path

    """
    motif = line_shape((0, 0), (line_length, 0))(subdivide_by_length(line_length, stitch_length))
    motif = rotate_by_degrees(repeat_stitches(motif, 2), angle)
    motif_generator = repeat_motif(motif)
    subdivision = remove_end(subdivision_by_length(stitch_length))

    return motif_to_points(motif_placement=subdivision_by_length(spacing),
                           line_subdivision=subdivision,
                           motif_generator=motif_generator)


def feather_stitch(spacing: float, stitch_width: float, stitch_length: float, repetitions: int):
    """
    Returns a stitch effect that is similar to the cretan stitch, but the lines pointing to the side are rotated.

    Args:
        spacing: The spacing between two spikes at the same side of the path
        stitch_width: The width of a line pointing to the side. Should be small, e.g. 0.5
        stitch_length: The length of a line pointing to the side.
        repetitions: How often a line pointing to the side is repeated.
    """
    motif = rotate_by_degrees(zigzag_motif(stitch_width, stitch_length, repetitions), 45) + (1, 0)
    motif_gen = repeat_motif_mirrored(motif)
    subdivision = subdivision_by_length(spacing)
    return motif_chain(subdivision, motif_gen, constant(0))


def overlock_stitch(length: float, width: float):
    """
    Returns a stitch effect that creates a stitch pattern along the path that resembles an overlock stitch.

    Args:
        length: The length of a single overlock stitch along the path
        width: The total width of the resulting stitch pattern
    """
    loop_ratio = 0.4
    motif = overlock_stitch_motif(width=1, height=1, loop_ratio=loop_ratio)
    stitch_effect = tile_motif(motif=motif, motif_length=length)
    back_stitch_subdivision = add_start(add_end(subdivision_by_length_with_offset(segment_length=length, offset=0.5)))

    def effect(path):
        constant_width_path = Path(path.shape, path.direction, constant(width), constant(0.5))
        left, right = get_boundaries(constant_width_path)
        back_stitch_offsets = back_stitch_subdivision(constant_width_path.length)
        back_stitch_line = inverse(mix(right, left, constant(loop_ratio)))

        stitches = stitch_effect(constant_width_path)
        back_stitches = back_stitch_line(back_stitch_offsets)

        return np.concatenate((stitches, right(1), left(1), back_stitches, back_stitches[-2::-1]))

    return effect


def rhomb_motif_stitch(spacing: float, width: float, length: float):
    """
    Returns a stitch effect that places rhombs along the path and connects them with a straight line.

    Args:
        spacing: The spacing between the centers of the rhombs
        width: The total width of the resulting stitch pattern
        length: The length of a rhomb along the path
    """
    motif = rotate_270(rhomb_motif(width, length))
    motif_gen = repeat_motif(motif)
    subdivision = subdivision_by_length(spacing)
    return motif_chain(subdivision, motif_gen, constant(0))


def stem_stitch(spacing: float, stitch_width: float, stitch_length: float, repetitions: int, angle: float):
    """
    Returns a stitch effect that imitates the look of a hand embroidered stem stitch. Each stitch is repeated multiple
    times to create the look of thick embroidery floss.

    Args:
        spacing: The spacing between the stitches
        stitch_width: The width of a single stitch. Should be small relative to the length, e.g. 0.5
        stitch_length: The length of a single stitch. Should be larger than spacing.
        repetitions: How often a single stitch is repeated to form a thick line
        angle: The rotation angle in degrees of the stitches relative to the direction of the path
    """
    motif = zigzag_rectangle(stitch_width, stitch_length, repetitions, horizontal=True)
    motif_generator = repeat_motif(motif)
    subdivision = subdivision_by_length_with_offset(segment_length=spacing, offset=0.5)

    return motif_chain(motif_placement=subdivision,
                       motif_generator=motif_generator,
                       motif_rotation_degrees=constant(angle))


def three_arrows(arrow_spacing: float, group_spacing: float, start_end_spacing: float, stitch_length: float):
    """
    Returns a stitch effect that creates a line along the path with groups of three arrows along the line.

    Args:
        arrow_spacing: The spacing between the three arrows of a group
        group_spacing: The spacing between groups of arrows
        start_end_spacing: The length of the line at the start and end which is kept free of arrows
        stitch_length: The length of the stitches of the running stitch line

    """
    single_arrow = np.array(((0, 0.0), (-3, -3), (0, 0), (-3, 3), (0, 0)))
    combined = np.concatenate((single_arrow, single_arrow + (arrow_spacing, 0), single_arrow + (arrow_spacing * 2, 0)))
    motif_subdivision = free_start(start_end_spacing, free_end(start_end_spacing, regular(group_spacing)))
    return motif_to_segments(motif_subdivision, regular(stitch_length), repeat_motif(combined), motif_length=3)


def x_motif_stitch(spacing: float, width: float, length: float):
    """
    Returns a stitch effect that places X-shapes along the path and connects them with a straight line.

    Args:
        spacing: The spacing between the centers of the X-shapes
        width: The total width of the resulting stitch pattern
        length: The length of an X-shape along the path
    """
    motif = rotate_by_degrees(x_motif(width, length), -90)
    motif_gen = repeat_motif(motif)
    subdivision = subdivision_by_length(spacing)
    return motif_chain(subdivision, motif_gen, constant(0))
