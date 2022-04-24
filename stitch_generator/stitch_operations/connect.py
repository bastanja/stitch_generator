import itertools

import numpy as np

from stitch_generator.framework.types import SamplingFunction
from stitch_generator.sampling.sampling_modifiers import remove_end, remove_start
from stitch_generator.stitch_effects.utilities.sample_line import sample_line


def connect(stitch_blocks, line_sampling_function: SamplingFunction):
    """
    Connects stitch blocks to one continuous stitch block by inserting stitches in the gaps between the blocks.
    Args:
        stitch_blocks:    stitch blocks to be connected
        line_sampling_function: the function that samples the connection line stitches between the end stitch of each
                                block and the start stitch the subsequent block

    Returns:
        A single stitch block containing all stitches from the stitch_blocks, connected with intermediate stitches
        between them
    """
    pairs = zip(stitch_blocks, stitch_blocks[1:])
    fills = [sample_line(p1[-1], p2[0], remove_start(remove_end(line_sampling_function))) for p1, p2 in pairs]

    parts = itertools.zip_longest(stitch_blocks, fills)

    combined = [i for i in itertools.chain.from_iterable(parts) if i is not None]
    return np.concatenate(combined)
