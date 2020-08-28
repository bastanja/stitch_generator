from stitch_generator.functions.function_modifiers import repeat, shift, add
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_2d import line, ellipse, constant_direction


def rounded_rect(width: float, height: float, corner_radius_x: float, corner_radius_y: float):
    corner = repeat(0.25, ellipse(corner_radius_x, corner_radius_y))

    down = line((width, corner_radius_y), (width, height - corner_radius_y))
    left = line((width - corner_radius_x, height), (corner_radius_x, height))
    up = line((0, height - corner_radius_y), (0, corner_radius_y))
    right = line((corner_radius_x, 0), (width - corner_radius_x, 0))

    corner1 = add(corner, constant_direction(width - corner_radius_x, height - corner_radius_y))
    corner2 = shift(1, add(corner, constant_direction(corner_radius_x, height - corner_radius_y)))
    corner3 = shift(2, add(corner, constant_direction(corner_radius_x, corner_radius_y)))
    corner4 = shift(3, add(corner, constant_direction(width - corner_radius_x, corner_radius_y)))

    return function_sequence((down, corner1, left, corner2, up, corner3, right, corner4))
