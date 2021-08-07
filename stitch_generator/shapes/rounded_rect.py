import itertools

from stitch_generator.functions.function_modifiers import repeat, multiply, inverse
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_2d import constant_direction
from stitch_generator.shapes.ellipse import ellipse
from stitch_generator.shapes.line import line


def corner(x, y, w, h):
    result = repeat(0.25, ellipse(w, h, center=(x - w, y - h)))
    return result


def rounded_rect_with_radius(width: float, height: float, corner_radius_x: float, corner_radius_y: float):
    return rounded_rect(width, height, [(corner_radius_x, corner_radius_y)] * 4)


def rounded_rect(width: float, height: float, corner_radii):
    corners = [corner(width / 2, height / 2, *radius) for radius in corner_radii]

    direction = itertools.cycle((lambda x: x, inverse))
    scale_x = (1, -1, -1, 1)
    scale_y = (1, 1, -1, -1)
    corners = [d(multiply(c, constant_direction(x, y))) for d, c, x, y in zip(direction, corners, scale_x, scale_y)]
    connections = [line(a(1), b(0)) for a, b in zip([corners[-1]] + corners[:-1], corners)]
    functions = list(itertools.chain.from_iterable(zip(connections, corners)))

    return function_sequence(functions)
