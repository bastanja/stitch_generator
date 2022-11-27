import numpy as np

from stitch_generator.sampling.sample_by_number import sample_by_number


def normal_length_one(direction) -> bool:
    samples = sample_by_number(1000)
    directions = direction(samples)
    lengths = np.linalg.norm(directions, axis=1)
    return np.allclose(lengths, 1)
