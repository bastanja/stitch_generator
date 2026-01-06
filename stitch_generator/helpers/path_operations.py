"""Path operations module for manipulating Path objects."""

from typing import List, Tuple

import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.framework.types import Function1D, CoordinateFunction, Function2D
from stitch_generator.functions.arc_length_mapping import arc_length_mapping
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import (
    split,
    inverse,
    mix,
    multiply,
    subtract,
    add,
    repeat,
    shift,
    maximum,
    divide,
    chain,
)
from stitch_generator.functions.functions_1d import constant

def default_width_and_alignment_path(shape: Function2D, direction: Function2D) -> Path:
    return Path(shape, direction, constant(1), constant(0.5))


def split_path(path: Path, offsets) -> List[Path]:
    """
    Splits a path at the given offsets

    Args:
        path: The path to split
        offsets: Split locations in the range [0, 1]

    Returns:
        A list of paths, from which each one represents the section of the original path between two offsets
    """
    shapes = split(path.shape, offsets)
    directions = split(path.direction, offsets)
    widths = split(path.width, offsets)
    stroke_alignments = split(path.stroke_alignment, offsets)
    return [Path(*params) for params in zip(shapes, directions, widths, stroke_alignments)]


def inverse_path(path: Path) -> Path:
    """
    Reverses the direction of the path

    Args:
        path: The path to reverse

    Returns:
        The reversed path
    """
    return apply_modifier_to_path(path, inverse)


def apply_modifier_to_path(path: Path, function_modifier) -> Path:
    """
    Applies a function modifier to all members of the Path

    Args:
        path: The path to modify
        function_modifier: A function that can be applied to 1D functions and coordinate functions
                          (functions that return coordinate points) and returns a function of the same type

    Returns:
        A Path where the function_modifier is applied to all members
    """
    shape = function_modifier(path.shape)
    direction = function_modifier(path.direction)
    width = function_modifier(path.width)
    stroke_alignment = function_modifier(path.stroke_alignment)
    return Path(shape, direction, width, stroke_alignment)


def path_from_boundaries(
    left: CoordinateFunction, right: CoordinateFunction, alignment: Function1D = constant(0.5)
) -> Path:
    """Creates a Path from left and right boundary functions.

    Constructs a path by calculating the center line and width from the left and
    right boundaries. The center line is interpolated between the boundaries
    based on the alignment parameter.

    Args:
        left: A function defining the left boundary of the path. Should accept
            parameters in [0, 1] and return coordinate arrays.
        right: A function defining the right boundary of the path. Should accept
            parameters in [0, 1] and return coordinate arrays of the same
            dimension as left.
        alignment: A 1D function defining the interpolation factor between left
            and right boundaries. Values in [0, 1]:
            - 0: Center line equals left boundary
            - 0.5: Center line is halfway between boundaries (default)
            - 1: Center line equals right boundary

    Returns:
        A new Path with the calculated shape, direction, width, and stroke_alignment.
    """
    position = mix(left, right, alignment)

    def width(t):
        delta = subtract(right, left)(t)
        return np.linalg.norm(delta, axis=1)

    def direction(t):
        return divide(subtract(right, left), width)(t)

    return Path(shape=position, direction=direction, width=width, stroke_alignment=alignment)


def get_boundaries(path: Path) -> Tuple[CoordinateFunction, CoordinateFunction]:
    """
    Calculates the left and right boundary functions of a path.

    Computes the boundary functions from the path's shape, direction, width, and
    stroke_alignment. The boundaries represent the outer edges of the path.

    Args:
        path: The path for which the boundaries are calculated.

    Returns:
        A tuple (left, right) containing:
        - left: A function defining the left boundary, returning coordinate arrays
        - right: A function defining the right boundary, returning coordinate arrays
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
    path_length = estimate_length(path.shape)
    if path_length < 2 * inset:
        return path
    cut = inset / path_length
    return apply_modifier_to_path(path, lambda function: repeat(1 - 2 * cut, (shift(cut, function))))


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

    return Path(shape=new_shape, direction=path.direction, width=new_width, stroke_alignment=path.stroke_alignment)


def parameterize_path_by_arc_length(path: Path, samples: int = 200):
    mapping = arc_length_mapping(path.shape, approximation_samples=samples)
    return apply_modifier_to_path(path, lambda function: chain(mapping, function))

def path_is_circular(path: Path):
    shape_start_end_equal = np.all(np.isclose(path.shape(0), path.shape(1)))
    direction_start_end_equal = np.all(np.isclose(path.direction(0), path.direction(1)))
    return shape_start_end_equal and direction_start_end_equal
