from pyembroidery import COMMAND_MASK, COLOR_BREAK
from stitch_generator.file_io.embroidery_export import to_pyembroidery
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern
from stitch_generator.functions.functions_2d import line
from stitch_generator.functions.sample import sample


def test_to_pyembroidery():
    # create embroidery pattern with two blocks
    pattern = EmbroideryPattern()
    pattern.add_stitches(sample(line(100, 0), 50))
    pattern.add_stitches(sample(line(100, 100), 50))

    # convert to pyembroidery format
    export_pattern = to_pyembroidery(pattern)

    # expect one stitch for each stitch plus one COLOR_BREAK for each block
    assert len(export_pattern.stitches) == pattern.number_of_stitches + len(pattern.stitch_blocks)

    # check that last stitch is the COLOR_BREAK
    last_stitch = export_pattern.stitches[-1]
    assert last_stitch[2] & COMMAND_MASK == COLOR_BREAK
