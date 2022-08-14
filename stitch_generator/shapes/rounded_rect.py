import itertools

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import repeat, multiply, inverse, shift
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_2d import constant_direction
from stitch_generator.shapes.circle import circle
from stitch_generator.shapes.ellipse import ellipse
from stitch_generator.shapes.line import line
from stitch_generator.stitch_operations.rotate import rotate_270


def corner(x, y, w, h):
    result = repeat(0.25, ellipse(w, h, center=(x - w, y - h)))
    return result


def rounded_rect_with_radius(width: float, height: float, corner_radius_x: float, corner_radius_y: float):
    return rounded_rect(width, height, [(corner_radius_x, corner_radius_y)] * 4)


def rounded_rect(width: float, height: float, corner_radii):
    corners = [corner(width / 2, height / 2, *radius) for radius in corner_radii]

    corner_scale_factors = itertools.cycle((lambda x: x, inverse))
    scale_x = (1, -1, -1, 1)
    scale_y = (1, 1, -1, -1)
    corners = [d(multiply(c, constant_direction(x, y))) for d, c, x, y in
               zip(corner_scale_factors, corners, scale_x, scale_y)]
    connections = [line(a(1), b(0)) for a, b in zip([corners[-1]] + corners[:-1], corners)]
    functions = list(itertools.chain.from_iterable(zip(connections, corners)))

    return function_sequence(functions)


def rounded_rect_with_direction(width: float, height: float, corner_radii):
    # alternating inverse of function direction
    corner_forward_backward = itertools.cycle((lambda function: function, inverse))

    # corner position scale factors
    scale_x = (1, -1, -1, 1)
    scale_y = (1, 1, -1, -1)

    # corner functions
    corners = [corner(width / 2, height / 2, *radius) for radius in corner_radii]
    corners = [d(multiply(c, constant_direction(x, y))) for d, c, x, y in
               zip(corner_forward_backward, corners, scale_x, scale_y)]

    corner_directions = [shift(i, (repeat(0.25, circle(), mode='wrap'))) for i in range(4)]

    # connecting line functions
    connection_points = [(a(1), b(0)) for a, b in zip([corners[-1]] + corners[:-1], corners)]

    connections = [line(a, b) for a, b in connection_points]
    connection_directions = [(b - a) for a, b in connection_points]
    connection_directions = [rotate_270(x)[0] for x in connection_directions]
    connection_directions = [constant_direction(d[0], d[1], normalized=True) for d in connection_directions]

    shapes = list(itertools.chain.from_iterable(zip(connections, corners)))
    directions = list(itertools.chain.from_iterable(zip(connection_directions, corner_directions)))

    lengths = [estimate_length(s) for s in shapes]

    return function_sequence(shapes, lengths), function_sequence(directions, lengths)
