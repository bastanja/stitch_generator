import numpy as np

from stitch_generator.functions.function_1d_stairs import stairs
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number


def test_stairs_two_steps():
    steps = subdivide_by_number(1)
    ratio = 0.1
    f = stairs(steps, ratio)

    # values at start, middle, end
    values = np.array((0, 0.5, 1))
    assert np.allclose(f(values), (0, 0.5, 1))

    # values immediately before and after the step
    step_increase_size = ratio / len(steps)
    values = np.array((0.5 - step_increase_size, 0.5 + step_increase_size))
    assert np.allclose(f(values), (0, 1))


def test_stairs_three_steps():
    steps = subdivide_by_number(2)
    ratio = 0.2
    f = stairs(steps, ratio)

    # values at start, middle, end
    values = np.array((0, 1 / 3, 0.5, 2 / 3, 1))
    assert np.allclose(f(values), (0, 0.25, 0.5, 0.75, 1))

    # values immediately before and after the step
    step_increase_size = ratio / len(steps)
    values = np.array((1 / 3 - step_increase_size, 1 / 3 + step_increase_size))
    assert np.allclose(f(values), (0, 0.5))
