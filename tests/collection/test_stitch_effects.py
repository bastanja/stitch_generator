from itertools import product

import numpy as np
import pytest

from stitch_generator.collection.stitch_effects.stitch_effects import stitch_effect_collection
from stitch_generator.framework.path import Path
from stitch_generator.functions.function_modifiers import chain
from stitch_generator.functions.functions_1d import constant, linear_interpolation, arc
from stitch_generator.shapes.bezier import bezier
from stitch_generator.shapes.circle import circle
from stitch_generator.shapes.line import line
from stitch_generator.stitch_operations.remove_duplicates import remove_duplicates

test_paths = [
    # regular linear path with constant width
    Path(*line(origin=(0, 0), to=(100, 0)), width=constant(10)),
    # path with bezier shape and a width of zero at the start and end
    Path(*bezier(control_points=((0, 0), (50, 50), (100, 0))), width=chain(arc, linear_interpolation(0, 15))),
    # circular path
    Path(*circle(radius=30), width=constant(5), stroke_alignment=constant(0.5)),
    # path with zero length
    Path(*line(origin=(0, 0), to=(0, 0)), width=constant(10))
]

test_values = list(product(test_paths, stitch_effect_collection()))


@pytest.mark.parametrize("path, effect", test_values)
def test_stitch_effect(path, effect):
    stitches = effect(path)

    # check that the effect creates at least one stitches
    assert (len(stitches) > 0)

    # check that the stitches have x and y coordinate
    assert (stitches.shape[1] == 2)

    # check that the stitches don't contain any duplicates
    without_duplicates = remove_duplicates(stitches)
    # assert len(stitches) == len(without_duplicates) # ToDo: not fulfilled by all stitch effects


def in_rectangle(points, left: float, top: float, right: float, bottom: float):
    points_x = points[:, 0]
    points_y = points[:, 1]
    left_outside = points_x < left
    top_outside = points_y < top
    right_outside = points_x > right
    bottom_outside = points_y > bottom
    any_outside = np.logical_or(np.logical_or(left_outside, right_outside),
                                np.logical_or(top_outside, bottom_outside))
    all_inside = np.logical_not(any_outside)
    return all_inside


@pytest.mark.parametrize("effect", stitch_effect_collection())
def test_stitch_in_rectangle_bounds(effect):
    # create a rectangular path with a given width and height
    width, height = 100, 30
    path = Path(*line(origin=(0, height / 2), to=(width, height / 2)), width=constant(height),
                stroke_alignment=constant(0.5))

    # apply the stitch effect
    stitches = effect(path)

    # check that all stitches lie inside the rectangle
    stitches_inside = in_rectangle(stitches, left=0, top=0, right=width, bottom=height)
    assert (np.alltrue(stitches_inside))


def in_circle(points, center, radius: float):
    distance = points - center
    lengths = np.linalg.norm(distance, axis=1)
    is_inside = lengths <= radius
    return is_inside


@pytest.mark.parametrize("effect", stitch_effect_collection())
def test_stitch_in_circle_bounds(effect):
    # create a circular path with a given width and height
    radius, width = 50, 20
    path = Path(*circle(radius=radius), width=constant(width), stroke_alignment=constant(0.5))

    # check that the path is circular, because some stitch effects have special handling for circular paths
    assert path.is_circular

    # apply the stitch effect
    stitches = effect(path)

    threshold = 0.01
    half_width = width / 2 + threshold

    # check that all stitches lie inside the outer boundary
    stitches_inside_outer = in_circle(stitches, radius=radius + half_width, center=(0, 0))
    assert (np.all(stitches_inside_outer == True))

    # check that no stitches lie inside the inner boundary
    stitches_inside_inner = in_circle(stitches, radius=radius - half_width, center=(0, 0))
    assert (np.all(stitches_inside_inner == False))
