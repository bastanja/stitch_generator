import numpy as np

from stitch_generator.functions.function_modifiers import repeat
from stitch_generator.functions.functions_1d import constant, linear_interpolation
from stitch_generator.functions.functions_2d import line, function_2d
from stitch_generator.functions.linspace import samples, mid_samples
from stitch_generator.stitch_effects.variable_running_stitch import variable_running_stitch


def test_variable_running_stitch():
    with_lists()
    with_generators()
    with_multiple_strokes()
    with_inner_gap()
    with_double_width_values()
    with_negative_direction()


def with_lists():
    positions = ((0, 0), (1, 0), (2, 0), (3, 0))
    directions = ((0, 1), (0, 1), (0, 1), (0, 1))
    widths = (0, 1, 0)
    min_strokes = 1
    max_strokes = 3

    stitches = variable_running_stitch(positions, directions, widths, min_strokes, max_strokes, 1)

    assert len(stitches) == 6
    expected_result = ((0, 0), (1, 0), (2, 1), (1, 1), (2, 0), (3, 0))
    assert np.allclose(stitches, expected_result)

    positions = ((0, 0), (10, 0), (20, 0), (30, 0))
    stitches = variable_running_stitch(positions, directions, widths, min_strokes, max_strokes, 1)
    expected_result = ((0, 0), (10, 0), (20, 1), (10, 1), (20, 0), (30, 0))
    assert np.allclose(stitches, expected_result)


def with_generators():
    params = samples(3, include_endpoint=True)
    mid = mid_samples(3)
    f = line(3, 0)
    d = function_2d(constant(0), constant(1))
    w = repeat(2, linear_interpolation(0, 1), 'reflect')
    min_strokes = 1
    max_strokes = 3

    stitches = variable_running_stitch(f(params), d(params), w(mid), min_strokes, max_strokes, 1)

    expected_result = ((0, 0), (1, 0), (2, 1), (1, 1), (2, 0), (3, 0))
    assert np.allclose(stitches, expected_result)


def with_multiple_strokes():
    params = samples(3, include_endpoint=True)
    f = line(3, 0)
    d = function_2d(constant(0), constant(1))
    widths = (0, 1, 0)
    min_strokes = 1
    max_strokes = 5

    stitches = variable_running_stitch(f(params), d(params), widths, min_strokes, max_strokes, 2)
    expected_result = ((0, 0), (1, 0), (2, 1), (1, 2), (2, 2), (1, 1), (2, 0), (3, 0))
    assert np.allclose(stitches, expected_result)


def with_inner_gap():
    f = line(5, 0)
    d = function_2d(constant(0), constant(1))
    widths = (0, 1, 0, 1, 0)
    params = samples(5, include_endpoint=True)
    min_strokes = 1
    max_strokes = 3

    stitches = variable_running_stitch(f(params), d(params), widths, min_strokes, max_strokes, 1)
    expected_result = ((0, 0), (1, 0), (2, 1), (1, 1), (2, 0), (3, 0), (4, 1), (3, 1), (4, 0), (5, 0))
    assert np.allclose(stitches, expected_result)


def with_double_width_values():
    f = line(4, 0)
    d = function_2d(constant(0), constant(1))
    widths = (0, 1, 1, 0)
    params = samples(4, include_endpoint=True)
    min_strokes = 1
    max_strokes = 3

    stitches = variable_running_stitch(f(params), d(params), widths, min_strokes, max_strokes, 1)
    expected_result = ((0, 0), (1, 0), (2, 0.5), (3, 1), (2, 1), (1, 1), (2, 0.5), (3, 0), (4, 0))
    assert np.allclose(stitches, expected_result)

    widths = (0, 0, 1, 1)
    stitches = variable_running_stitch(f(params), d(params), widths, min_strokes, max_strokes, 1)
    expected_result = ((0, 0), (1, 0), (2, 0), (3, 0.5), (4, 1), (3, 1), (2, 1), (3, 0.5), (4, 0))
    assert np.allclose(stitches, expected_result)

    widths = (1, 1, 0, 0)
    stitches = variable_running_stitch(f(params), d(params), widths, min_strokes, max_strokes, 1)
    expected_result = ((0, 0), (1, 0.5), (2, 1), (1, 1), (0, 1), (1, 0.5), (2, 0), (3, 0), (4, 0))
    assert np.allclose(stitches, expected_result)


def with_negative_direction():
    positions = ((0, 0), (1, 0), (2, 0), (3, 0))
    directions = ((0, -1), (0, -1), (0, -1), (0, -1))
    widths = (0, 1, 0)
    min_strokes = 1
    max_strokes = 3

    stitches = variable_running_stitch(positions, directions, widths, min_strokes, max_strokes, 1)

    assert len(stitches) == 6
    expected_result = ((0, 0), (1, 0), (2, -1), (1, -1), (2, 0), (3, 0))
    assert np.allclose(stitches, expected_result)
