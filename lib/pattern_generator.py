import numpy as np


def constant_pattern(stitch_pattern: np.ndarray):
    """
    generator function which returns a copy of the same pattern each time
    """
    while True:
        yield stitch_pattern.copy()


def cycle_patterns(stitch_patterns):
    """
    generator function which cycles through a list of patterns
    """
    while True:
        for s in stitch_patterns:
            yield s.copy()
