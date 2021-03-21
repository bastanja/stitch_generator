import pytest

from stitch_generator.designs.design_collection import designs
from stitch_generator.framework.embroidery_pattern import EmbroideryPattern


@pytest.mark.parametrize("design", designs)
def test_all_designs(design):
    pattern = design().get_pattern(parameters={})
    assert type(pattern) == EmbroideryPattern
    assert len(pattern.stitch_blocks) > 0
