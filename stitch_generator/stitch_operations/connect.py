import itertools

import numpy as np


def connect(stitch_blocks, connect_function):
    """
    Connects several separate stitch blocks to one continuous stitch block by inserting stitches in the gaps between the
    blocks.
    Args:
        stitch_blocks:    stitch blocks to be connected
        connect_function: the function that provides stitches between the en stitch of each block and the start stitch
                          the subsequent block

    Returns:
        A single stitch block containing all stitches from the stitch_blocks, connected with intermediate stitches
        between them
    """
    pairs = zip(stitch_blocks, stitch_blocks[1:])
    fills = [connect_function(p1[-1], p2[0])[1:-1] for p1, p2 in pairs]

    parts = itertools.zip_longest(stitch_blocks, fills)

    combined = [i for i in itertools.chain.from_iterable(parts) if i is not None]
    return np.concatenate(combined)
