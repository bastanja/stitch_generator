from stitch_generator.functions.function_modifiers import shift, repeat, subtract, maximum, multiply, add
from stitch_generator.functions.functions_1d import constant
from stitch_generator.framework.path import Path


def get_underlay_path(path: Path, inset: float) -> Path:
    """
    Calculates a path that is smaller than the original path by the size of 'inset'. Such a path lies completely inside
    the original path and can therefore be used for underlays.

    Args:
        path:  The path for which the underlay path is calculated
        inset: The amount by which the resulting path is smaller. inset is subtracted from the width and from the total
               length of the path. Inset should be a positive value. Negative values are only supported if all members
               of the original path support being evaluated outside the range [0, 1]

    Returns:
        The underlay path
    """
    cut = inset / path.length
    underlay = path.apply_modifier(lambda function: repeat(1 - 2 * cut, (shift(cut, function))))

    # calculate the middle of the stroke, relative to the center line 'underlay.shape'
    to_middle = add(underlay.stroke_alignment, constant(-0.5))
    middle_relative_to_old_width = multiply(to_middle, underlay.width)

    # subtract inset * 2 from the width and make sure it stays positive
    new_width = maximum(subtract(underlay.width, constant(inset * 2)), constant(0))

    # calculate offset of the new center line relative to middle of the stroke
    offset = multiply(to_middle, multiply(constant(-1), new_width))
    new_pos_offset = add(middle_relative_to_old_width, offset)

    new_shape = add(underlay.shape, multiply(underlay.direction, new_pos_offset))

    return Path(shape=new_shape, direction=underlay.direction, width=new_width,
                stroke_alignment=underlay.stroke_alignment)
