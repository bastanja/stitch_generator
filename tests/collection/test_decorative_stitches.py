from itertools import product

import pytest

from stitch_generator.collection.stitch_effects.decorative_stitches import decorative_stitches_collection
from stitch_generator.framework.path import Path
from stitch_generator.shapes.bezier import bezier
from stitch_generator.shapes.line import line
from stitch_generator.stitch_operations.remove_duplicates import remove_duplicates

test_paths = [
    Path(*line(origin=(0, 0), to=(100, 0))),
    Path(*bezier(control_points=((0, 0), (50, 50), (100, 0))))
]

test_values = list(product(test_paths, decorative_stitches_collection()))


@pytest.mark.parametrize("path, effect", test_values)
def test_stitch_effect(path, effect):
    stitches = effect(path)

    # check that the effect creates at least two stitches
    assert (len(stitches) > 1)

    # check that the stitches have x and y coordinate
    assert (stitches.shape[1] == 2)

    # check that the stitches don't contain any duplicates
    assert len(stitches) == len(remove_duplicates(stitches))
