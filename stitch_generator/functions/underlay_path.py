from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import shift, repeat, subtract, maximum, multiply, add
from stitch_generator.functions.functions_1d import constant
from stitch_generator.functions.path import Path


def underlay_path(path: Path, inset: float) -> Path:
    cut = inset / estimate_length(path.position)
    underlay = path.apply_modifier(lambda function: repeat(1 - 2 * cut, (shift(cut, function))))

    middle_alignment = add(underlay.stroke_alignment, constant(-0.5))
    with_width = multiply(middle_alignment, underlay.width)
    with_direction = multiply(underlay.direction, with_width)
    position = add(underlay.position, with_direction)

    width = maximum(subtract(underlay.width, constant(inset * 2)), constant(0))

    return Path(position=position, direction=underlay.direction, width=width,
                stroke_alignment=constant(0.5))
