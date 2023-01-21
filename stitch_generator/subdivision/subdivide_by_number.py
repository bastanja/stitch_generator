import numpy as np

from stitch_generator.framework.types import SubdivisionFunction, Array1D


def subdivide_by_number(number_of_segments: int) -> Array1D:
    return np.linspace(0, 1, num=number_of_segments + 1, endpoint=True)


def subdivision_by_number(number_of_segments: int) -> SubdivisionFunction:
    def f(total_length: float):
        return subdivide_by_number(number_of_segments=number_of_segments)

    return f
