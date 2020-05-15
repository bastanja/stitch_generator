import pytest

from stitch_generator.functions.embroidery_pattern import EmbroideryPattern


def test_add_stitches():
    p = EmbroideryPattern()
    with pytest.raises(Exception):
        p.add_stitches([])

    # add stitches without color
    p.add_stitches([(0, 1), (2, 3), (4, 5)])

    # add stitches with color
    p.add_stitches([(10, 11), (12, 13), (14, 15)], 0x000000)


def test_get_stitch():
    p = EmbroideryPattern()
    p.add_stitches([(0, 0), (2, 2), (4, 4)], 0x0080FF)
    p.add_stitches([(10, 0), (12, 2), (14, 4)], 0x008000)

    # get stitch from first stitch block
    assert p.get_stitch(0) == (0, 0)

    # get last stitch from first stitch block
    assert p.get_stitch(2) == (4, 4)

    # get stitch from second stitch block
    assert p.get_stitch(3) == (10, 0)

    # get last stitch
    assert p.get_stitch(5) == (14, 4)

    # try getting a stitch at an invalid index
    with pytest.raises(Exception):
        p.get_stitch(6)

    with pytest.raises(Exception):
        p.get_stitch(-1)


def test_number_of_stitches():
    p = EmbroideryPattern()
    assert p.number_of_stitches == 0
    stitches = [(0, 0), (2, 2), (4, 4)]
    p.add_stitches(stitches, 0x0080FF)
    assert p.number_of_stitches == len(stitches)

    p.add_stitches(stitches, 0x0080FF)
    assert p.number_of_stitches == len(stitches) * 2
