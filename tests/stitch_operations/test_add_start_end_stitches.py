import pytest

from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number
from stitch_generator.shapes.line import line_shape
from stitch_generator.stitch_operations.add_start_end_stitches import add_start_end_stitches
from stitch_generator.stitch_operations.remove_duplicates import remove_duplicates


@pytest.mark.parametrize("number_of_segments, number_of_repeated_segments", [
    (10, 3),
    (10, 5),
    (100, 1),
    (100, 0),
    (3, 3)
])
def test_add_start_end_stitches(number_of_segments, number_of_repeated_segments):
    shape = line_shape(origin=(0, 0), to=(10, 0))
    stitches = shape(subdivide_by_number(number_of_segments))

    # verify that we have the expected number of stitches before calling add_start_end_stitches
    number_of_stitches = number_of_segments + 1
    assert len(stitches) == number_of_stitches

    with_start_end = add_start_end_stitches(stitches, repeated_segments=number_of_repeated_segments)

    # check that the function does not create any duplicates
    assert len(with_start_end) == len(remove_duplicates(with_start_end))

    new_length = len(with_start_end)

    assert new_length == number_of_stitches + (2 * 2 * number_of_repeated_segments)
