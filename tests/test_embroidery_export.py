from pyembroidery import COMMAND_MASK, COLOR_BREAK

from stitch_generator.file_io.embroidery_export import to_pyembroidery
from stitch_generator.framework.embroidery_pattern import EmbroideryPattern
from stitch_generator.sampling.sample_by_length import regular
from stitch_generator.stitch_effects.utilities.sample_line import sample_line


def test_to_pyembroidery():
    sampling = regular(segment_length=3)

    # create embroidery pattern with two blocks
    pattern = EmbroideryPattern()
    pattern.add_stitches(sample_line((0, 0), (100, 0), sampling))
    pattern.add_stitches(sample_line((0, 0), (100, 100), sampling))

    # convert to pyembroidery format
    export_pattern = to_pyembroidery(pattern)

    # expect one stitch for each stitch plus one COLOR_BREAK for each block
    assert len(export_pattern.stitches) == pattern.number_of_stitches + len(pattern.stitch_blocks)

    # check that last stitch is the COLOR_BREAK
    last_stitch = export_pattern.stitches[-1]
    assert last_stitch[2] & COMMAND_MASK == COLOR_BREAK
