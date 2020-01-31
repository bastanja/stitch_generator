from pyembroidery import EmbPattern, COLOR_CHANGE, write_vp3

from file_io.embroidery_import import from_pyembroidery
from lib.functions_2d import line
from lib.sample import sample


def test_from_pyembroidery():
    # create embroidery pattern with two blocks
    pattern = EmbPattern()

    stitches1 = sample(line(90, 0), 10)
    stitches1 = stitches1.tolist()
    pattern.add_block(stitches1, 0x808080)

    stitches2 = sample(line(0, 90), 10)
    stitches2 = stitches2.tolist()
    pattern.add_block(stitches2, 0x000000)

    # convert from pyembroidery format
    import_pattern = from_pyembroidery(pattern)

    # expect one stitch for each stitch plus one COLOR_BREAK for each block
    # plus one for the manual color change
    assert len(pattern.stitches) == import_pattern.number_of_stitches + len(import_pattern.stitch_blocks)

