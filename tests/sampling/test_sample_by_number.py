import numpy as np

from stitch_generator.sampling.sample_by_number import linspace


def test_linspace():
    segments = 10
    length = 5

    with_endpoint = linspace(0, length, segments, include_endpoint=True)
    no_endpoint = linspace(0, length, segments, include_endpoint=False)

    reference = [length / segments * i for i in range(segments + 1)]

    assert len(with_endpoint) == segments + 1
    assert len(no_endpoint) == segments
    assert np.allclose(with_endpoint[:-1], no_endpoint)
    assert np.allclose(with_endpoint, reference)
