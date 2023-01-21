import numpy as np

from stitch_generator.subdivision.change_subdivision import change_subdivision_by_length, change_subdivision, \
    change_subdivision_by_segment
from stitch_generator.subdivision.subdivide_by_fixed_length import subdivision_by_fixed_length
from stitch_generator.subdivision.subdivide_by_length import subdivision_by_length
from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number, subdivision_by_number
from stitch_generator.shapes.line import line_shape


def test_change_subdivision_by_length():
    f = line_shape((0, 0), (10, 0))
    stitches = f(subdivide_by_number(10))

    newly_subdivided = change_subdivision_by_length(stitches, segment_length=2)
    assert len(newly_subdivided) == 6
    assert np.allclose(newly_subdivided, f(subdivide_by_number(5)))

    newly_subdivided = change_subdivision_by_length(stitches, 0.2)
    assert len(newly_subdivided) == 51
    assert np.allclose(newly_subdivided, f(subdivide_by_number(50)))


def subdivision_functions():
    yield subdivision_by_length(segment_length=3)
    yield subdivision_by_fixed_length(segment_length=2, alignment=0, offset=0)
    yield subdivision_by_number(number_of_segments=3)


def test_change_subdivision():
    total_length = 10

    f = line_shape((0, 0), (total_length, 0))
    stitches = f(subdivide_by_number(100))

    for subdivision_function in iter(subdivision_functions()):
        values = f(subdivision_function(total_length))
        newly_subdivided = change_subdivision(stitches, subdivision_function)
        assert np.allclose(values, newly_subdivided)


def test_change_subdivision_by_segment():
    polyline = ((0, 50), (0, 0), (50, 0))
    result = change_subdivision_by_segment(points=polyline, segment_length=10)
    length = result.shape[0]
    assert length == 11
    assert np.allclose(result[0], polyline[0])
    assert np.allclose(result[5], polyline[1])
    assert np.allclose(result[-1], polyline[-1])
