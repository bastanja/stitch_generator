from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import shift, repeat, subtract, maximum, multiply, add
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.path import Path


def get_underlay_path(path: Path, inset: float) -> Path:
    cut = inset / estimate_length(path.position)
    underlay = path.apply_modifier(lambda function: repeat(1 - 2 * cut, (shift(cut, function))))

    # calculate the middle of the stroke, relative to the center line 'underlay.position'
    to_middle = add(underlay.stroke_alignment, constant(-0.5))
    middle_relative_to_old_width = multiply(to_middle, underlay.width)

    # subtract inset * 2 from the width and make sure it stays positive
    new_width = maximum(subtract(underlay.width, constant(inset * 2)), constant(0))

    # calculate offset of the new center line relative to middle of the stroke
    offset = multiply(to_middle, multiply(constant(-1), new_width))
    new_pos_offset = add(middle_relative_to_old_width, offset)

    new_position = add(underlay.position, multiply(underlay.direction, new_pos_offset))

    return Path(position=new_position, direction=underlay.direction, width=new_width,
                stroke_alignment=underlay.stroke_alignment)
