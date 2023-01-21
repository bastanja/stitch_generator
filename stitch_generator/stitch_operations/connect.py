import itertools
from typing import List

import numpy as np

from stitch_generator.framework.types import SubdivisionFunction, Array2D
from stitch_generator.subdivision.subdivision_modifiers import remove_end, remove_start
from stitch_generator.stitch_effects.utilities.subdivide_line import subdivide_line


def connect(stitch_blocks: List[Array2D], line_subdivision: SubdivisionFunction) -> Array2D:
    """
    Connects stitch blocks to one continuous stitch block by inserting stitches in the gaps between the blocks.
    Args:
        stitch_blocks:    stitch blocks to be connected
        line_subdivision: the function that subdivides the connection line stitches between the end stitch of each
                                block and the start stitch the subsequent block

    Returns:
        A single stitch block containing all stitches from the stitch_blocks, connected with intermediate stitches
        between them
    """
    if len(stitch_blocks) < 1:
        return np.array([])
    if len(stitch_blocks) == 1:
        return stitch_blocks[0]

    pairs = zip(stitch_blocks, stitch_blocks[1:])
    fills = [subdivide_line(p1[-1], p2[0], remove_start(remove_end(line_subdivision))) for p1, p2 in pairs]

    parts = itertools.zip_longest(stitch_blocks, fills)

    combined = [i for i in itertools.chain.from_iterable(parts) if i is not None]
    return np.concatenate(combined)
