import numpy as np

from stitch_generator.subdivision.subdivide_by_number import subdivide_by_number


def normal_length_one(direction) -> bool:
    directions = direction(subdivide_by_number(1000))
    lengths = np.linalg.norm(directions, axis=1)
    return np.allclose(lengths, 1)
