import numpy as np
import pytest

from stitch_generator.sampling.sample_by_number import sample_by_number


@pytest.mark.parametrize("number_of_segments", [1, 5, 10])
def test_sample_by_number(number_of_segments):
    with_endpoint = sample_by_number(number_of_segments)

    reference = [1 / number_of_segments * i for i in range(number_of_segments + 1)]

    assert len(with_endpoint) == number_of_segments + 1
    assert np.allclose(with_endpoint, reference)
