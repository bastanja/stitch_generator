from pyembroidery import COMMAND_MASK, COLOR_BREAK

from stitch_generator.file_io.embroidery_export import to_pyembroidery
from stitch_generator.functions.connect_functions import running_stitch_line
from stitch_generator.functions.embroidery_pattern import EmbroideryPattern


def test_to_pyembroidery():
    # create embroidery pattern with two blocks
    pattern = EmbroideryPattern()
    stitch_effect = running_stitch_line(stitch_length=3, include_endpoint=True)
    pattern.add_stitches(stitch_effect((0, 0), (100, 0)))
    pattern.add_stitches(stitch_effect((0, 0), (100, 100)))

    # convert to pyembroidery format
    export_pattern = to_pyembroidery(pattern)

    # expect one stitch for each stitch plus one COLOR_BREAK for each block
    assert len(export_pattern.stitches) == pattern.number_of_stitches + len(pattern.stitch_blocks)

    # check that last stitch is the COLOR_BREAK
    last_stitch = export_pattern.stitches[-1]
    assert last_stitch[2] & COMMAND_MASK == COLOR_BREAK
