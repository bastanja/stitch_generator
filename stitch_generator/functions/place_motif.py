from stitch_generator.stitch_effects.rotate import rotate


def place_motif_at(position, direction, scale, stitch_pattern, include_endpoint=False):
    if len(stitch_pattern) == 0:
        return position
    stitch_pattern = stitch_pattern.copy()
    stitch_pattern *= scale
    stitch_pattern = rotate(stitches=stitch_pattern, sin=direction[1], cos=direction[0])
    stitch_pattern += position
    last = None if include_endpoint else -1
    return stitch_pattern[0:last]
