import numpy as np
from stitch_generator.framework.path import Path
from stitch_generator.framework.stitch_effect import StitchEffect
from stitch_generator.framework.types import Array2D, Function2D, Function1D
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import mix
from stitch_generator.functions.functions_1d import constant, linear_interpolation
from stitch_generator.subdivision.subdivide_by_length import subdivide_by_length
from stitch_generator.stitch_effects.utilities.motif_to_path import motif_to_path
from stitch_generator.stitch_effects.utilities.range_tree import make_range_tree, tree_to_indices_and_offsets


def variable_running_stitch(stitch_length: float, width_profile: Function1D, min_strokes: int, max_strokes: int,
                            stroke_spacing: float) -> StitchEffect:
    """

    Args:
        stitch_length: The stitch length of the stitch effect
        width_profile: defines how wide the stitch line should. width values should be between 0 and 1. Where the width
            is 0, the resulting stitch line will be repeated `min_strokes` times. Where width is 1, the resulting stitch
            line will be repeated `max_strokes` times.
        min_strokes: defines how often the stitch line is repeated at its thinnest locations. Should be an odd number.
             If it is an even number, the line will be repeated at least min_strokes + 1 times.
        max_strokes: defines how often the stitch line is repeated at its widest locations. Should be an odd number.
             If it is an even number, the line will be repeated at most max_strokes - 1 times.
        stroke_spacing: The distance between two stokes. Should be small, e.g. 0.2

    Returns:
        A StitchEffect

    """
    return lambda path: variable_running_stitch_on_shape(path.shape, path.direction, stitch_length=stitch_length,
                                                         width_profile=width_profile, min_strokes=min_strokes,
                                                         max_strokes=max_strokes, stroke_spacing=stroke_spacing)


def variable_running_stitch_on_shape(shape: Function2D, direction: Function2D, stitch_length: float,
                                     width_profile: Function1D, min_strokes: int, max_strokes: int,
                                     stroke_spacing: float = 0.2) -> Array2D:
    total_length = estimate_length(shape)
    t = subdivide_by_length(total_length=total_length, segment_length=stitch_length)

    widths = width_profile(t)
    widths = np.minimum(widths[0:-1], widths[1:])

    levels = width_to_level(widths, min_strokes, max_strokes)

    width_level_tree = make_range_tree(levels)
    indices, offsets = tree_to_indices_and_offsets(width_level_tree)

    motif = np.vstack((indices, offsets)).astype(float).T

    max_level = _to_level_rounding_up(max_strokes)

    motif[:, 0] /= float(len(widths))
    if max_level > 0:
        motif[:, 1] /= max_level

    min_level = _to_level_rounding_down(min_strokes)
    max_level = _to_level_rounding_up(max_strokes)
    min_alignment = (min_level / max_level if max_level > 0 else 0) * 0.5
    alignment = mix(constant(min_alignment), constant(0.5), factor=width_profile)

    path = Path(shape=shape, direction=direction, width=constant(max_level * stroke_spacing),
                stroke_alignment=alignment)

    return motif_to_path(motif=motif, path=path)


def width_to_level(width, min_strokes: int, max_strokes: int):
    """
    Converts a width values in the range [0, 1] to their corresponding thickness level

    Args:
        width: An array of width values
        min_strokes: The minimum amount of strokes the resulting running stitch should have
        max_strokes: The maximum amount of strokes the resulting running stitch should have

    Returns:
        An array of levels
    """

    # clamp width between 0 and 1
    width[width < 0] = 0
    width[width > 1] = 1

    # Scale width to the range between the minimum level and one above the maximum level
    # Add one to maximum, because we round down to the lower integer value
    max_level = _to_level_rounding_up(max_strokes)
    to_level = linear_interpolation(_to_level_rounding_down(min_strokes), max_level + 1)

    # round level down to integer value
    level = to_level(width)
    level = np.floor(level).astype(int)

    # keep level below maximum level
    level[level > max_level] = max_level

    return level


def _to_level_rounding_down(strokes: int):
    return int(strokes / 2)


def _to_level_rounding_up(strokes: int):
    return int((strokes - 1) / 2)
