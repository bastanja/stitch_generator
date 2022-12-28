import itertools
from typing import Sequence, Tuple

from stitch_generator.framework.types import Function2D
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import repeat, multiply, inverse, shift
from stitch_generator.functions.function_sequence import function_sequence
from stitch_generator.functions.functions_2d import constant_direction
from stitch_generator.shapes.ellipse import ellipse_shape, ellipse_direction
from stitch_generator.shapes.line import line


def simple_rounded_rect(width: float, height: float, corner_radius) -> Tuple[Function2D, Function2D]:
    return rounded_rect(width, height, [(corner_radius, corner_radius)] * 4)


def rounded_rect_with_corner_radii(width: float, height: float, corner_radii: Sequence[float]) \
        -> Tuple[Function2D, Function2D]:
    return rounded_rect(width, height, [(r, r) for r in corner_radii])


def rounded_rect(width: float, height: float, corner_radii):
    shapes = _shape_parts(width=width, height=height, corner_radii=corner_radii)
    directions = _direction_parts(corner_radii=corner_radii)
    lengths = [estimate_length(s) for s in shapes]
    return function_sequence(shapes, lengths), function_sequence(directions, lengths)


def _shape_parts(width: float, height: float, corner_radii):
    # alternating inverse of function direction
    corner_forward_backward = itertools.cycle((lambda function: function, inverse))

    # corner position scale factors
    scale_x = (1, -1, -1, 1)
    scale_y = (1, 1, -1, -1)

    # corner functions
    corners = [_corner(width / 2, height / 2, *radius) for radius in corner_radii]
    corners = [d(multiply(c, constant_direction(x, y))) for d, c, x, y in
               zip(corner_forward_backward, corners, scale_x, scale_y)]

    # connecting line functions
    connection_points = [(a(1), b(0)) for a, b in zip([corners[-1]] + corners[:-1], corners)]
    connections = [line(a, b)[0] for a, b in connection_points]

    shapes = list(itertools.chain.from_iterable(zip(connections, corners)))

    return shapes


def _direction_parts(corner_radii):
    corner_directions = [(repeat(0.25, ellipse_direction(rx=x, ry=y), mode='wrap')) for x, y in corner_radii]
    corner_directions = [shift(i, f) for i, f in zip(range(4), corner_directions)]
    connection_directions = [constant_direction(x, y) for x, y in ((1, 0), (0, 1), (-1, 0), (0, -1))]
    directions = list(itertools.chain.from_iterable(zip(connection_directions, corner_directions)))
    return directions


def _corner(x, y, w, h):
    result = repeat(0.25, ellipse_shape(w, h, center=(x - w, y - h)))
    return result
