import numpy as np

from stitch_generator.framework.path import Path
from stitch_generator.functions.estimate_length import estimate_length
from stitch_generator.functions.function_modifiers import add, multiply, subtract, inverse, scale
from stitch_generator.functions.functions_1d import linear_interpolation, constant, smootherstep
from stitch_generator.functions.get_boundaries import get_boundaries
from stitch_generator.sampling.sample_by_number import sample_by_number
from stitch_generator.sampling.sampling_modifiers import add_start
from stitch_generator.sampling.tatami_sampling import tatami_sampling
from stitch_generator.framework.types import Function1D, Array2D


def variable_running_stitch_along(path: Path, stroke_spacing: float, stitch_length: float) -> Array2D:
    segments = int(round(estimate_length(path.shape) / stitch_length))
    t = sample_by_number(number_of_segments=segments)

    widths = path.width(t)
    widths = np.minimum(widths[0:-1], widths[1:])

    levels = _width_to_level(widths, stroke_spacing)

    width_level_tree = _make_range_tree(levels)
    indices, offsets = _tree_to_indices_and_offsets(width_level_tree)

    positions = path.shape(t)
    directions = path.direction(t)
    alignment = (1 - path.stroke_alignment(t)) * path.width(t)
    positions = positions - (directions * alignment[:, None])

    positions = np.array([positions[i] for i in indices])
    directions = np.array([directions[i] for i in indices])

    offsets = np.array(offsets, dtype=float)[:, None]
    offsets *= stroke_spacing

    directions = directions * offsets
    return positions + directions


def variable_underlay_along(path: Path, stroke_spacing: float, stitch_length: float) -> Array2D:
    pos1 = add(path.shape, multiply(path.direction, multiply(path.width, path.stroke_alignment)))
    width1 = multiply(path.width, path.stroke_alignment)
    path1 = Path(shape=pos1, direction=path.direction, width=width1, stroke_alignment=constant(0))

    pos2 = inverse(add(path.shape,
                       multiply(path.direction, multiply(path.width, subtract(path.stroke_alignment, constant(1))))))
    width2 = inverse(multiply(path.width, subtract(constant(1), path.stroke_alignment)))
    dir2 = inverse(multiply(path.direction, constant(-1)))
    path2 = Path(shape=pos2, direction=dir2, width=width2, stroke_alignment=constant(0))

    step_function = smootherstep

    return np.concatenate((_variable_underlay(path1, stroke_spacing, stitch_length, step_function)[:-1],
                           _variable_underlay(path2, stroke_spacing, stitch_length, step_function)))


def _variable_underlay(path: Path, stroke_spacing: float, stitch_length: float, step_function: Function1D):
    precision = 10
    segments = int(round(estimate_length(path.shape) * precision))
    t = sample_by_number(number_of_segments=segments)

    widths = path.width(t)
    widths = np.minimum(widths[0:-1], widths[1:])

    levels = _width_to_level(widths, stroke_spacing)

    width_level_tree = _make_range_tree(levels)
    indices, offsets = _tree_to_indices_and_offsets_basic(width_level_tree)

    sampling_function = add_start(tatami_sampling(segment_length=stitch_length, offsets=(0, 1 / 3, 2 / 3), alignment=0.5,
                                                  minimal_segment_size=0.25))

    stitches = []
    iopairs = list(zip(indices, offsets))
    baseline = path.shape
    for p1, p2 in zip(iopairs, iopairs[1:]):
        i1, o1 = p1
        i2, o2 = p2

        t1, t2 = t[i1], t[i2]
        path_part = path.split([t1, t2])[1]
        _, baseline = get_boundaries(path_part)
        level_step = add(constant(o1 * stroke_spacing), scale((o2 - o1) * stroke_spacing, step_function))
        direction = multiply(path_part.direction, level_step)
        baseline = add(baseline, direction)
        part_length = estimate_length(baseline)
        stitches.append(baseline(sampling_function(part_length)))

    stitches.append(baseline(1))
    stitches = np.concatenate(stitches)
    return stitches


def _width_to_level(widths: np.ndarray, level_spacing: float):
    widths = widths / level_spacing
    widths = np.maximum(widths, 0)  # avoid negative values
    return widths.astype(int)


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
        samples = sample_by_number(number_of_segments=len(level_indices) - 1)[:-1]
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
        samples = sample_by_number(number_of_segments=len(level_indices) - 1)[:-1]
        offsets.extend(linear_interpolation(level, level - 1)(samples))

    assert len(indices) == len(offsets)
    return indices, offsets


def _tree_to_indices_and_offsets_basic(tree, level=0):
    indices = []
    offsets = []

    # indices between which we fill the current level
    level_indices = tree.get_range(not _is_reverse(level))

    # remember start index in order to fill gaps later
    start_index = level_indices[-1]

    children = tree.children

    indices.append(level_indices[-1])
    offsets.append(level)

    first = True
    for i in tree.get_children_range(_is_reverse(level)):
        child_indices = children[i].get_range(_is_reverse(level))

        # fill the gap before this range
        direction = 1
        if _is_reverse(level):
            direction = -1
        gap_indices = range(start_index, child_indices[0], direction)

        if len(gap_indices) > 1 and not first:
            indices.append(gap_indices[0])
            indices.append(gap_indices[-1])
            offsets.append(level)
            offsets.append(level)

        # add the child range
        ind, off = _tree_to_indices_and_offsets_basic(children[i], level + 1)
        indices.extend(ind)
        offsets.extend(off)

        # update start index for gap in next loop iteration
        start_index = child_indices[-1]

        first = False

    indices.append(level_indices[0])
    offsets.append(level)

    assert len(indices) == len(offsets)
    return indices, offsets
