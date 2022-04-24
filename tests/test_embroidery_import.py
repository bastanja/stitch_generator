from pyembroidery import EmbPattern

from stitch_generator.file_io.embroidery_import import from_pyembroidery
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.stitch_effects.utilities.sample_line import sample_line


def test_from_pyembroidery():
    # create embroidery pattern with two blocks
    pattern = EmbPattern()

    sampling = regular(segment_length=3)

    stitches1 = sample_line((0, 0), (100, 0), sampling)
    stitches1 = stitches1.tolist()
    pattern.add_block(stitches1, 0x808080)

    stitches2 = sample_line((0, 0), (0, 100), sampling)
    stitches2 = stitches2.tolist()
    pattern.add_block(stitches2, 0x000000)

    # convert from pyembroidery format
    import_pattern = from_pyembroidery(pattern)

    # expect one stitch for each stitch plus one COLOR_BREAK for each block
    # plus one for the manual color change
    assert len(pattern.stitches) == import_pattern.number_of_stitches + len(import_pattern.stitch_blocks)
