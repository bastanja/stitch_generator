import numpy as np
import pytest

from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number


@pytest.mark.parametrize("number_of_segments", [1, 5, 10])
def test_subdivide_by_number(number_of_segments):
    values = subdivide_by_number(number_of_segments)

    reference = [1 / number_of_segments * i for i in range(number_of_segments + 1)]

    assert len(values) == number_of_segments + 1
    assert np.allclose(values, reference)
