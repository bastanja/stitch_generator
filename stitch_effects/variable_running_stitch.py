import numpy as np
from lib.functions_1d import linear_interpolation
from lib.sample import sample
from typing import Iterable, Tuple


def variable_running_stitch(positions: Iterable[Tuple[float]],
                            directions: Iterable[Tuple[float]],
                            widths: Iterable[float],
                            min_strokes: int,
                            max_strokes: int,
                            width_scale: float):
    """
    Creates a running stitch with variable width. Width is achieved by stitching back and forth with a slight offset
    to the side until the desired line width is reached. The width can vary along the course of the stitch line. This
    means that a part of the stitch line can stitched only once and appear very thin while another part is stitched
    multiple times and therefore appear wider.

    Parameters:
        positions: defines the positions of the stitches

        directions: defines in which direction the stitches are moved for the repetitions. There should be a
            direction for each stitch. The direction should usually be perpendicular to the stitch line at that position
            and be a normalized vector.

        widths: defines for each segment between two positions how wide the stitch line should be at this segment. When
            n positions are provided, widths should have length n-1. width values should be between 0 and 1. Where the
            width is 0, the resulting stitch line will be repeated `min_strokes` times. Where width is 1, the resulting
            stitch line will be repeated `max_strokes` times.

        min_strokes: defines how often the stitch line is repeated at its thinnest locations. Should be an odd number.
            If it is an even number, the line will be repeated at least min_strokes + 1 times.

        max_strokes: defines how often the stitch line is repeated at its widest locations. Should be an odd number.
            If it is an even number, the line will be repeated at most max_strokes - 1 times.

        width_scale: defines how wide the variable running stitch is at its widest location. If it is 0, the repeating
            stitches will be exactly at the locations defined by `positions`. If it is not 0, width_scale defines how
            far the stitches will be moved into the `direction` at the widest location.
    """

    width_to_level = _get_width_to_level_function(min_strokes, max_strokes)
    levels = [width_to_level(w) for w in widths]
    width_level_tree = _make_range_tree(levels)
    indices, offsets = _tree_to_indices_and_offsets(width_level_tree)

    # make sure we have lists (not generators), because we need to access them with index
    positions = list(positions)
    directions = list(directions)

    positions = np.array([positions[i] for i in indices])
    directions = np.array([directions[i] for i in indices])

    offsets = np.array(offsets, dtype=float)[:, None]
    offsets *= width_scale / width_to_level(1)

    directions = directions * offsets
    return positions + directions


def _get_width_to_level_function(min_strokes, max_strokes):
    """
    Returns a function that converts width values in the range between 0 and 1 to integer values representing width
    levels. A level of 0 means that the stroke is repeated one time, level 1 means it is repeated three times, level 2
    means the stroke is repeated five times etc.
    """
    to_level = linear_interpolation(_to_min(min_strokes), _to_max(max_strokes) + 1)

    def f(w):
        val = 0 if w < 0 else 1 if w > 1 else w
        level = to_level(val) - 0.5
        level = int(round(level))
        level = min(level, _to_max(max_strokes))
        return level

    return f


def _to_min(strokes: int):
    return int(strokes / 2)


def _to_max(strokes: int):
    return int((strokes - 1) / 2)


def _make_range_tree(values):
    stack = []
    _start_range(stack, 0)
    root = stack[0]

    prev_value = 0
    for i, value in enumerate(values):
        delta = value - prev_value
        prev_value = value

        if delta > 0:
            for _ in range(delta):
                _start_range(stack, i)

        if delta < 0:
            for _ in range(-delta):
                _end_range(stack, i)

    for i in range(len(stack)):
        _end_range(stack, len(values))

    return root


class _Interval:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.children = []

    def get_range(self, reverse):
        interval = range(self.start, self.end + 1)
        if reverse:
            interval = _reverse_range(interval)
        return interval

    def get_children_range(self, reverse):
        interval = range(len(self.children))
        if reverse:
            interval = _reverse_range(interval)
        return interval


def _start_range(stack, index):
    interval = _Interval()
    interval.start = index

    if len(stack) > 0:
        stack[-1].children.append(interval)

    stack.append(interval)


def _end_range(stack, index):
    interval = stack.pop()
    interval.end = index


def _reverse_range(interval):
    return range(interval.stop - 1, interval.start - 1, -interval.step)


def _is_reverse(level):
    return level % 2 == 1  # odd numbers treated as reverse


def _tree_to_indices_and_offsets(tree, level=0):
    indices = []
    offsets = []

    # indices between which we fill the current level
    level_indices = tree.get_range(not _is_reverse(level))

    # remember start index in order to fill gaps later
    start_index = level_indices[-1]

    # start to end, level up
    if level > 0:
        indices.extend(list(level_indices[0:-1]))
        offsets.extend(sample(linear_interpolation(level - 1, level), len(level_indices) - 1, False))

    children = tree.children

    for i in tree.get_children_range(_is_reverse(level)):
        # fill the gap before this range
        child_indices = children[i].get_range(_is_reverse(level))
        direction = 1
        if _is_reverse(level):
            direction = -1
        gap_indices = range(start_index, child_indices[0], direction)

        if len(gap_indices) > 0:
            indices.extend(list(gap_indices))
            offsets.extend([level] * len(gap_indices))

        # add the child range
        i, o = _tree_to_indices_and_offsets(children[i], level + 1)
        indices.extend(i)
        offsets.extend(o)

        # update start index for gap in next loop iteration
        start_index = child_indices[-1]

    # fill the gap after last child range
    direction = 1
    if _is_reverse(level):
        direction = -1
    gap_indices = range(start_index, level_indices[0], direction)

    if len(gap_indices) > 0:
        indices.extend(gap_indices)
        offsets.extend([level] * len(gap_indices))

    # start to end, level down
    if level == 0:
        indices.append(level_indices[0])
        offsets.append(level)
    else:
        indices.extend(level_indices[0:-1])
        offsets.extend(sample(linear_interpolation(level, level - 1), len(level_indices) - 1, False))

    assert len(indices) == len(offsets)
    return indices, offsets
