from pyembroidery import EmbPattern

from stitch_generator.file_io.embroidery_import import from_pyembroidery
from stitch_generator.functions.connect_functions import running_stitch_line


def test_from_pyembroidery():
    # create embroidery pattern with two blocks
    pattern = EmbPattern()

    stitch_effect = running_stitch_line(stitch_length=3, include_endpoint=True)

    stitches1 = stitch_effect((0, 0), (100, 0))
    stitches1 = stitches1.tolist()
    pattern.add_block(stitches1, 0x808080)

    stitches2 = stitch_effect((0, 0), (0, 100))
    stitches2 = stitches2.tolist()
    pattern.add_block(stitches2, 0x000000)

    # convert from pyembroidery format
    import_pattern = from_pyembroidery(pattern)

    # expect one stitch for each stitch plus one COLOR_BREAK for each block
    # plus one for the manual color change
    assert len(pattern.stitches) == import_pattern.number_of_stitches + len(import_pattern.stitch_blocks)
