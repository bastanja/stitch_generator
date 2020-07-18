import numpy as np

from stitch_generator.functions.samples import linspace, linspace_mid, samples_by_length, samples_by_fixed_length


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


def _test_samples_by_length(total_length, segment_length, expected_segments):
    with_endpoint = samples_by_length(total_length, segment_length, include_endpoint=True)
    no_endpoint = samples_by_length(total_length, segment_length, include_endpoint=False)

    with_endpoint = with_endpoint
    no_endpoint = no_endpoint

    reference = [1 / expected_segments * i for i in range(expected_segments + 1)]

    assert len(with_endpoint) == expected_segments + 1
    assert len(no_endpoint) == expected_segments
    assert np.allclose(with_endpoint[:-1], no_endpoint)
    assert np.allclose(with_endpoint, reference)


def test_samples_by_length():
    # test where segments fit into length exactly
    _test_samples_by_length(total_length=10, segment_length=2, expected_segments=5)
    _test_samples_by_length(total_length=12, segment_length=2, expected_segments=6)

    # test with half segment
    _test_samples_by_length(total_length=10.49, segment_length=2, expected_segments=5)
    _test_samples_by_length(total_length=11, segment_length=2, expected_segments=6)
    _test_samples_by_length(total_length=11.01, segment_length=2, expected_segments=6)

    # test with segment length which is larger than the total length
    _test_samples_by_length(total_length=5, segment_length=10, expected_segments=1)

    # test with total length of zero
    _test_samples_by_length(total_length=0, segment_length=10, expected_segments=1)

    # check that segment length of zero raises an exception
    with pytest.raises(Exception):
        _test_samples_by_length(total_length=5, segment_length=0, expected_segments=1)


def _test_samples_by_fixed_length(total_length, segment_length, expected_segments):
    samples = samples_by_fixed_length(total_length, segment_length)

    segment_length_relative = 0
    if total_length > 0:
        segment_length_relative = segment_length / total_length

    reference = [segment_length_relative * i for i in range(expected_segments + 1)]

    assert len(samples) == expected_segments + 1
    assert np.allclose(samples, reference)


def test_samples_by_fixed_length():
    # test where segments fit into length exactly
    _test_samples_by_fixed_length(total_length=10, segment_length=2, expected_segments=5)
    _test_samples_by_fixed_length(total_length=12, segment_length=2, expected_segments=6)

    # test with partial segment
    _test_samples_by_fixed_length(total_length=9.99, segment_length=2, expected_segments=4)
    _test_samples_by_fixed_length(total_length=10.01, segment_length=2, expected_segments=5)
    _test_samples_by_fixed_length(total_length=11.99, segment_length=2, expected_segments=5)

    # test with segment length which is larger than the total length
    _test_samples_by_fixed_length(total_length=5, segment_length=10, expected_segments=0)

    # test with total length of zero
    _test_samples_by_fixed_length(total_length=0, segment_length=10, expected_segments=0)

    # check that segment length of zero raises an exception
    with pytest.raises(Exception):
        _test_samples_by_fixed_length(total_length=5, segment_length=0, expected_segments=0)


def test_linspace_mid():
    samples = linspace_mid(start=0, stop=10, number_of_segments=5)
    assert np.allclose(samples, (1, 3, 5, 7, 9))

    samples = linspace_mid(start=0, stop=10, number_of_segments=2)
    assert np.allclose(samples, (2.5, 7.5))
