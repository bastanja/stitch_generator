import numpy as np

from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.functions_1d import linear_interpolation
from stitch_generator.functions.path import Path
from stitch_generator.functions.samples import samples_by_segments, mid_samples_by_segments
from stitch_generator.functions.sampling import segment_sampling


def variable_running_stitch(path: Path, stroke_spacing: float, stitch_length: float):
    segments = int(round(estimate_length(path.position) / stitch_length))
    t = samples_by_segments(number_of_segments=segments, include_endpoint=True)
    c = mid_samples_by_segments(number_of_segments=segments)

    widths = path.width(c)
    levels = width_to_level(widths, stroke_spacing)

    width_level_tree = _make_range_tree(levels)
    indices, offsets = _tree_to_indices_and_offsets(width_level_tree)

    positions = path.position(t)
    directions = path.direction(t)

    positions = np.array([positions[i] for i in indices])
    directions = np.array([directions[i] for i in indices])

    offsets = np.array(offsets, dtype=float)[:, None]
    offsets *= stroke_spacing

    directions = directions * offsets
    return positions + directions


def width_to_level(widths: np.ndarray, level_spacing: float):
    widths = np.round(widths / level_spacing)
    widths = np.maximum(widths, 0)  # avoid negative values
    return widths.astype(int)


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
        samples = samples_by_segments(number_of_segments=len(level_indices) - 1, include_endpoint=False)
        offsets.extend(linear_interpolation(level - 1, level)(samples))

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
        samples = samples_by_segments(number_of_segments=len(level_indices) - 1, include_endpoint=False)
        offsets.extend(linear_interpolation(level, level - 1)(samples))

    assert len(indices) == len(offsets)
    return indices, offsets
