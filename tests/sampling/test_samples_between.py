import numpy as np

from stitch_generator.sampling.sample_by_length import sampling_by_length
from stitch_generator.sampling.samples_between import samples_between


def test_samples_between():
    total_length = 10
    sampling_function = sampling_by_length(segment_length=1)

    # test sampling full range between 0 and 1
    full_samples = sampling_function(total_length)
    samples = samples_between(total_length=total_length, start_offset=0, end_offset=1,
                              sampling_function=sampling_function)
    assert (np.allclose(full_samples, samples))

    # test sampling of partial range
    samples = samples_between(total_length=total_length, start_offset=0.25, end_offset=0.75,
                              sampling_function=sampling_function)
    assert (np.alltrue(samples >= 0.25))
    assert (np.alltrue(samples <= 0.75))
    assert (len(samples) >= 2)
