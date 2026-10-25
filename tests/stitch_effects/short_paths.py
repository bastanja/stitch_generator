from itertools import product

import numpy as np

from tests.paths import line_path, tapered_bezier_path

short_paths = {
    f"line_{length}_width_{width}": line_path(
        origin=(0, 0), to=(length, 0), width=width
    )
    for length, width in product((0, 1e-6, 0.01, 0.1, 0.5, 1, 2), (0, 0.5, 6))
}
# short curved path with a width of zero at the start and end
short_paths["bezier"] = tapered_bezier_path(
    control_points=((0, 0), (0.5, 0.5), (1, 0)), max_width=2
)


def assert_at_least_two_stitches(stitches):
    # a stitch effect returns at least a start and an end point
    assert stitches.ndim == 2
    assert stitches.shape[1] == 2
    assert len(stitches) >= 2
    assert np.all(np.isfinite(stitches))
