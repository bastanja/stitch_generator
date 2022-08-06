import numpy as np

from stitch_generator.stitch_operations.rotate import rotate_by_sin_cos


def place_motif_at(position, direction, scale, motif, include_endpoint=False):
    if len(motif) == 0:
        return position
    motif = motif.copy()
    motif *= scale
    motif = rotate_by_sin_cos(stitches=motif, sin=direction[1], cos=direction[0])
    motif += position
    last = None if include_endpoint else -1
    return motif[0:last]


def place_motif_between(p1, p2, motif, include_endpoint=False, width_scale=None):
    if len(motif) == 0:
        return p1

    if np.allclose(p1, p2):
        return p1

    motif = _normalize_motif(motif)
    delta = p2 - p1
    scale_x = np.linalg.norm(delta)

    scale_y = scale_x
    if width_scale:
        scale_y *= width_scale

    delta /= scale_x

    motif *= (scale_x, scale_y)
    motif = rotate_by_sin_cos(motif, delta[1], delta[0])
    motif += p1

    last = None if include_endpoint else -1
    return motif[0:last]


def _normalize_motif(motif):
    motif = np.asarray(motif, dtype=float).copy()
    p1, p2 = motif[0], motif[-1]
    d = p2 - p1
    size = np.linalg.norm(d)
    motif -= p1
    motif /= size
    d /= size
    return rotate_by_sin_cos(motif, -d[1], d[0])
