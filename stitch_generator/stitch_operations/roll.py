import numpy as np


def roll(stitches, amount):
    modified = stitches.copy()
    modified[1::] = np.roll(stitches[1::], amount, axis=0)
    modified[0] = modified[-1]
    return modified
