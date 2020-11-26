import numpy as np

from stitch_generator.stitch_operations.remove_duplicates import remove_duplicates


def test_remove_duplicates():
    expected_result = np.array(((0.0, 0), (1, 1), (2, 2)))

    points = np.array(((0.0, 0), (1, 1), (1, 1), (2, 2)))
    result = remove_duplicates(points)
    assert(np.allclose(result, expected_result))

    points = np.array(((0.0, 0), (1, 1), (1, 1), (1, 1), (2, 2)))
    result = remove_duplicates(points)
    assert(np.allclose(result, expected_result))
