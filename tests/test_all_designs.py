from stitch_generator.designs.design_collection import designs
from stitch_generator.framework.embroidery_pattern import EmbroideryPattern


def test_all_designs():
    for d in designs:
        pattern = d().get_pattern(parameters={})
        assert type(pattern) == EmbroideryPattern
        assert len(pattern.stitch_blocks) > 0
