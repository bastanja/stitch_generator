import numpy as np
from pyembroidery import EmbPattern, read_vp3

from stitch_generator.functions.embroidery_pattern import EmbroideryPattern


def from_pyembroidery(pyembroidery_pattern: EmbPattern):
    scale_factor = 1 / 10  # convert from to embroidery file scale 1/10 mm to millimeters
    result = EmbroideryPattern()

    if not pyembroidery_pattern.stitches:
        return result

    for block, col in pyembroidery_pattern.get_as_colorblocks():
        stitches = np.array(block)

        # Third value of each stitch is a flag which defines the stitch type.
        # Select only the column which contains the flags of all stitches
        flags = stitches[:, 2]

        # Array of booleans which is True if the stitch flag is 0
        is_regular_stitch = flags == 0

        # Slice to select only the stitches which are regular stitches
        regular_stitches = stitches[is_regular_stitch]

        # Slice to select only the x and y coordinates of the stitches
        regular_stitches = regular_stitches[:, 0:2]

        # Apply the scale factor
        scaled_stitches = regular_stitches * scale_factor

        # Add them to the EmbroideryPattern
        result.add_stitches(scaled_stitches, col.color)

    return result


def import_vp3(filename):
    pyembroidery_pattern = read_vp3(filename)
    return from_pyembroidery(pyembroidery_pattern)
