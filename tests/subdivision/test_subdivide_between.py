import numpy as np

from stitch_generator.subdivision.subdivide_by_length import subdivision_by_length
from stitch_generator.subdivision.subdivide_between import subdivide_between


def test_subdivide_between():
    total_length = 10
    subdivision = subdivision_by_length(segment_length=1)

    # test subdivision full range between 0 and 1
    all_values = subdivision(total_length)
    values = subdivide_between(total_length=total_length, start_offset=0, end_offset=1,
                               subdivision_function=subdivision)
    assert (np.allclose(all_values, values))

    # test subdivision of partial range
    values = subdivide_between(total_length=total_length, start_offset=0.25, end_offset=0.75,
                               subdivision_function=subdivision)
    assert (np.alltrue(values >= 0.25))
    assert (np.alltrue(values <= 0.75))
    assert (len(values) >= 2)
