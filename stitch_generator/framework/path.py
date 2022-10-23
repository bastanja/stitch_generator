from typing import Tuple

import numpy as np

from stitch_generator.framework.types import Function1D, Function2D
from stitch_generator.functions.arc_length_mapping import arc_length_mapping
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import split, inverse, mix, multiply, subtract, add, repeat, shift, \
    maximum, divide, chain
from stitch_generator.functions.functions_1d import constant


class Path:
    def __init__(self, shape: Function2D, direction: Function2D, width: Function1D = constant(1),
                 stroke_alignment: Function1D = constant(0.5)):
        """
        Creates a Path

        Args:
            shape:            A 2D function that defines the baseline of the path
            direction:        A 2D function that defines the direction along the path. Usually perpendicular to the
                              tangent of the baseline, pointing to the left side of the path
            width:            A 1D function that defines the width of the path
            stroke_alignment: A 1D function that defines how much of the path is left of the baseline. 0 means the left
                              side of the path is equal to the baseline. 1 means that the right side of the path is
                              equal to the baseline. 0.5 means that the path is centered around the baseline.
        """
        self.shape = shape
        self.direction = direction
        self.width = width
        self.stroke_alignment = stroke_alignment
        self._length = None

    def split(self, offsets):
        """
        Splits a path at the given offsets

        Args:
            offsets: Split locations in the range [0, 1]

        Returns:
            A list of paths, from which each one represents the section of the original path between two offsets
        """
        shapes = split(self.shape, offsets)
        directions = split(self.direction, offsets)
        widths = split(self.width, offsets)
        stroke_alignments = split(self.stroke_alignment, offsets)
        return [Path(*params) for params in zip(shapes, directions, widths, stroke_alignments)]

    def inverse(self):
        """
        Reverses the direction of the path

        Returns:
            The reversed path
        """
        return self.apply_modifier(inverse)

    def apply_modifier(self, function_modifier):
        """
        Applies a function modifier to all members of the Path
        Args:
            function_modifier: A function that can be applied to 1DFunctions and 2DFunctions and returns a function of
                               the same type

        Returns:
            A Path where the function_modifier is applied to all members
        """
        shape = function_modifier(self.shape)
        direction = function_modifier(self.direction)
        width = function_modifier(self.width)
        stroke_alignment = function_modifier(self.stroke_alignment)
        return Path(shape, direction, width, stroke_alignment)

    @property
    def length(self):
        if self._length:
            return self._length
        return estimate_length(self.shape)

    @length.setter
    def length(self, value):
        self._length = value

    @property
    def is_circular(self):
        shape_start_end_equal = np.all(np.isclose(self.shape(0), self.shape(1)))
        direction_start_end_equal = np.all(np.isclose(self.direction(0), self.direction(1)))
        return shape_start_end_equal and direction_start_end_equal


def path_from_boundaries(left, right, alignment=constant(0.5)):
    position = mix(left, right, alignment)

    def width(t):
        delta = subtract(right, left)(t)
        return np.linalg.norm(delta, axis=1)

    def direction(t):
        return divide(subtract(right, left), width)(t)

    return Path(shape=position, direction=direction, width=width, stroke_alignment=alignment)


def get_boundaries(path: Path) -> Tuple[Function2D, Function2D]:
    """
    Calculates the left and right boundary of a path

    Args:
        path: The path for which the boundaries are calculated

    Returns:
        left and right boundary of the path
    """
    positive_width = multiply(path.width, path.stroke_alignment)
    negative_width = multiply(path.width, subtract(constant(1), path.stroke_alignment))

    left = add(path.shape, multiply(path.direction, positive_width))
    right = subtract(path.shape, multiply(path.direction, negative_width))

    return left, right


def get_inset_path(path: Path, inset: float) -> Path:
    """
    Calculates a path that is smaller than the original path by the size of 'inset'. Such a path lies completely inside
    the original path and can therefore be used for underlays.

    Args:
        path:  The path for which the underlay path is calculated
        inset: The amount by which the resulting path is smaller. inset is subtracted from the width and from the total
               length of the path. Inset should be a positive value. Negative values are only supported if all members
               of the original path support being evaluated outside the range [0, 1]

    Returns:
        The underlay path
    """

    return inset_sides(cut_start_end(path, inset), inset)


def cut_start_end(path: Path, inset: float) -> Path:
    # if the shape is too short to subtract the inset, return the path itself
    if path.length < 2 * inset:
        return path
    cut = inset / path.length
    return path.apply_modifier(lambda function: repeat(1 - 2 * cut, (shift(cut, function))))


def inset_sides(path: Path, inset: float) -> Path:
    # calculate the middle of the stroke, relative to the center line 'underlay.shape'
    to_middle = add(path.stroke_alignment, constant(-0.5))
    middle_relative_to_old_width = multiply(to_middle, path.width)

    # subtract inset * 2 from the width and make sure it stays positive
    new_width = maximum(subtract(path.width, constant(inset * 2)), constant(0))

    # calculate offset of the new center line relative to middle of the stroke
    offset = multiply(to_middle, multiply(constant(-1), new_width))
    new_pos_offset = add(middle_relative_to_old_width, offset)

    new_shape = add(path.shape, multiply(path.direction, new_pos_offset))

    return Path(shape=new_shape, direction=path.direction, width=new_width,
                stroke_alignment=path.stroke_alignment)


def parameterize_path_by_arc_length(path: Path, samples: int = 200):
    mapping = arc_length_mapping(path.shape, approximation_samples=samples)
    return path.apply_modifier(lambda function: chain(mapping, function))
