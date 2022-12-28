import numpy as np

from stitch_generator.sampling.sample_by_length import sampling_by_length
from stitch_generator.stitch_operations.connect import connect


def test_connect():
    # two blocks
    block1 = np.array(((0, 10), (0, 0)))
    block2 = np.array(((30, 0), (30, 10)))
    sampling = sampling_by_length(segment_length=10)
    result = connect([block1, block2], sampling)

    assert np.allclose(result, ((0, 10), (0, 0), (10, 0), (20, 0), (30, 0), (30, 10)))

    # one block
    result = connect([block1], sampling)
    assert np.allclose(result, block1)

    # no block
    result = connect([], sampling)
    assert np.allclose(result, [])
