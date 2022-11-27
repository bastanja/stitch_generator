import numpy as np
import pytest

from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.shapes.circle import circle
from tests.shapes.normal_length import normal_length_one


@pytest.mark.parametrize("center, radius", [
    ((0, 0), 5),
    ((10, 10), 5),  # center not zero
    ((10, 10), 0),  # radius zerotest_circle.py
])
def test_circle(center, radius):
    shape, direction = circle(center=center, radius=radius)

    # check that directions are normalized
    assert normal_length_one(direction)

    # check that circle is closed
    assert np.allclose(shape(0), shape(1))

    # check that the distance to the center is equal for each point
    samples = sample_by_number(1000)
    positions = shape(samples)
    distances = positions - center
    lengths = np.linalg.norm(distances, axis=1)
    assert np.allclose(lengths, radius)
