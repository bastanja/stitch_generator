import numpy as np

from stitch_generator.functions.pattern_generator import constant_pattern, cycle_patterns


def test_constant_pattern():
    pattern = np.array(((0, 0), (1, 1), (2, 0), (3, 1)))
    pattern_generator = constant_pattern(pattern)

    # check that the generator returns equal patterns
    for _ in range(10):
        p = next(pattern_generator)
        assert np.allclose(pattern, p)

    # check that the returned pattern is a copy by modifying it and
    # verifying that the original pattern is still unchanged
    p[0] = (10, 10)
    assert np.allclose(p[0], (10, 10))
    assert np.allclose(pattern[0], (0, 0))


def test_cycle_patterns():
    p1 = np.array(((1, 0), (0, 0)))
    p2 = np.array(((2, 0), (0, 0)))
    p3 = np.array(((3, 0), (0, 0)))

    pattern_generator = cycle_patterns([p1, p2, p3])

    # check that each pattern is returned once
    assert np.allclose(p1, next(pattern_generator))
    assert np.allclose(p2, next(pattern_generator))
    assert np.allclose(p3, next(pattern_generator))

    # check that the first pattern is returned again after the last
    assert np.allclose(p1, next(pattern_generator))

    # check that a copy was returned by modifying the generated
    # pattern and expecting that the original remains unchanged
    p2_copy = next(pattern_generator)
    p2_copy[0] = (100, 100)
    assert np.allclose(p2[0], (2, 0))
