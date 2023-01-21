import itertools

import numpy as np

from stitch_generator.framework.types import SubdivisionFunction
from stitch_generator.functions.ensure_shape import ensure_1d_shape
from stitch_generator.functions.function_modifiers import chain


def alternate_direction(subdivision_function: SubdivisionFunction):
    """
    Returns the values from the subdivision_function in alternating direction by reversing them on every second call
    """
    forward = itertools.cycle((True, False))

    def modify(values):
        if not next(forward) and len(values) > 0:
            values = np.flip(1 - values, axis=0)

        return values

    return chain(subdivision_function, modify)


def ensure_value_at(subdivision_function: SubdivisionFunction, position: float):
    """ Moves the value which is nearest to position exactly to position """

    def modify(values):
        if len(values) == 0:
            return ensure_1d_shape(position)
        delta = np.abs(values - position)
        nearest_index = np.argmin(delta)
        values[nearest_index] = position
        return values

    return chain(subdivision_function, modify)


def add_start(subdivision_function: SubdivisionFunction) -> SubdivisionFunction:
    """ Adds a value at the start if it is missing """

    def modify(values):
        if len(values) > 0:
            if not np.isclose(values[0], 0):
                return np.concatenate((ensure_1d_shape(0), values))
            else:
                return values
        return ensure_1d_shape(0)

    return chain(subdivision_function, modify)


def add_end(subdivision_function: SubdivisionFunction) -> SubdivisionFunction:
    """ Adds a value at the end if it is missing """

    def modify(values):
        if len(values) > 0:
            if not np.isclose(values[-1], 1):
                return np.concatenate((values, ensure_1d_shape(1)))
            else:
                return values
        return ensure_1d_shape(1)

    return chain(subdivision_function, modify)


def remove_start(subdivision_function: SubdivisionFunction) -> SubdivisionFunction:
    """ Removes the first value from the subdivision function if it is close to the start """

    def modify(values):
        if len(values) > 0 and np.isclose(values[0], 0):
            return values[1:]
        return values

    return chain(subdivision_function, modify)


def remove_end(subdivision_function: SubdivisionFunction) -> SubdivisionFunction:
    """ Removes the last value from the subdivision function if it is close to the end """

    def modify(values):
        if len(values) > 0 and np.isclose(values[-1], 1):
            return values[:-1]
        return values

    return chain(subdivision_function, modify)


def free_start(start_length: float, subdivision_function: SubdivisionFunction):
    """ Removes the values which are closer to the start than start_length """

    def f(total_length: float):
        relative_length = (start_length / total_length) if (total_length > 0) else 0
        values = subdivision_function(total_length)
        values = values[values >= relative_length]
        return values

    return f


def free_end(end_length: float, subdivision_function: SubdivisionFunction):
    """ Removes the values which are closer to the end than end_length """

    def f(total_length: float):
        relative_length = (end_length / total_length) if (total_length > 0) else 0
        values = subdivision_function(total_length)
        values = values[values <= 1 - relative_length]
        return values

    return f


def cycle_offsets(partial_subdivision, offsets):
    offset_gen = itertools.cycle(offsets)

    def f(total_length: float):
        return partial_subdivision(offset=next(offset_gen), total_length=total_length)

    return f


def cycle_alignments(partial_subdivision, alignments):
    alignment_gen = itertools.cycle(alignments)

    def f(total_length: float):
        return partial_subdivision(alignment=next(alignment_gen), total_length=total_length)

    return f
