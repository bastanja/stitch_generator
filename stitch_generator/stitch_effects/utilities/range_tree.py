import numpy as np

# Helpers for stitch effects that repeat a line a variable number of times along a path.
#
# The path is sampled at points t[0..n]. For each of the n segments between two
# neighbouring points there is an integer level: level 0 means the segment is stitched
# once, and each additional level adds one back-and-forth pass on top of it.
#
# make_range_tree() turns the levels into a tree of nested index ranges, and the
# tree_to_indices_and_offsets* functions walk this tree to produce a single continuous
# stitch route as pairs of (point index, level offset).


def width_to_level(widths: np.ndarray, level_spacing: float):
    # every full level_spacing of width adds one level
    widths = widths / level_spacing
    widths = np.maximum(widths, 0)  # avoid negative values
    return widths.astype(int)


def make_range_tree(values):
    # Builds a tree of ranges: the root covers all points, and each node at depth d
    # is a maximal range of points in which every segment has a level of at least d.
    # Nodes are nested, i.e. the children of a node lie within the node's range.
    #
    # The stack holds the currently open range of each depth, so its length is
    # always the current level plus one (for the root).
    stack = []
    _start_range(stack, 0)
    root = stack[0]

    prev_value = 0
    for i, value in enumerate(values):
        delta = value - prev_value
        prev_value = value

        # level goes up: open one new (nested) range per level, starting at point i
        if delta > 0:
            for _ in range(delta):
                _start_range(stack, i)

        # level goes down: close the innermost ranges, ending at point i
        if delta < 0:
            for _ in range(-delta):
                _end_range(stack, i)

    # close all ranges that are still open (including the root) at the last point
    for i in range(len(stack)):
        _end_range(stack, len(values))

    return root


class _Interval:
    # a node of the range tree: the inclusive point range [start, end] and nested ranges
    def __init__(self):
        self.start = 0
        self.end = 0
        self.children = []

    def get_range(self, reverse):
        # point indices of this range, optionally from end to start
        interval = range(self.start, self.end + 1)
        if reverse:
            interval = _reverse_range(interval)
        return interval

    def get_children_range(self, reverse):
        # positions in self.children, optionally from last to first
        interval = range(len(self.children))
        if reverse:
            interval = _reverse_range(interval)
        return interval


def _start_range(stack, index):
    interval = _Interval()
    interval.start = index

    # the new range is nested in the currently innermost open range
    if len(stack) > 0:
        stack[-1].children.append(interval)

    stack.append(interval)


def _end_range(stack, index):
    interval = stack.pop()
    interval.end = index


def _reverse_range(interval):
    return range(interval.stop - 1, interval.start - 1, -interval.step)


def _is_reverse(level):
    # the route walks even levels forward along the path and odd levels backward,
    # which makes it go back and forth
    return level % 2 == 1  # odd numbers treated as reverse


# Events of the tree traversal, see _traverse()
_ENTER, _GAP, _EXIT = "enter", "gap", "exit"


def _traverse(tree, level=0):
    # list of (event, level, data) tuples in stitching order:
    # (_ENTER, level, level indices), (_GAP, level, (gap indices, is_first, is_last)),
    # (_EXIT, level, level indices)
    #
    # Each node at level > 0 is covered three times: on _ENTER the route moves along
    # the node's range from level - 1 up to the level, it then walks back over the
    # range at the level (gaps and children), and on _EXIT it moves along the range
    # again from the level down to level - 1.
    events = []
    _collect_events(tree, level, events)
    return events


def _collect_events(tree, level, events):
    # indices between which we fill the current level, ordered against this level's
    # walking direction: the walk at this level starts at level_indices[-1] and ends
    # at level_indices[0]
    level_indices = tree.get_range(not _is_reverse(level))
    direction = -1 if _is_reverse(level) else 1

    events.append((_ENTER, level, level_indices))

    # remember start index in order to fill gaps later
    start_index = level_indices[-1]

    children = tree.children

    # visit the children in walking direction
    for n, i in enumerate(tree.get_children_range(_is_reverse(level))):
        # the gap before this range: the points at the current level until the child
        # range begins (child_indices[0] is the child's first point in walking direction)
        child_indices = children[i].get_range(_is_reverse(level))
        gap_indices = range(start_index, child_indices[0], direction)
        events.append((_GAP, level, (gap_indices, n == 0, False)))

        # the child range
        _collect_events(children[i], level + 1, events)

        # update start index for gap in next loop iteration: the child's events end
        # on its last point in walking direction
        start_index = child_indices[-1]

    # the gap after last child range
    gap_indices = range(start_index, level_indices[0], direction)
    events.append((_GAP, level, (gap_indices, False, True)))

    events.append((_EXIT, level, level_indices))


def tree_to_indices_and_offsets(tree, level=0):
    # Returns every point of the stitch route: for each stitch the index of its point
    # on the path and its offset in levels. The offset changes linearly while moving
    # between levels, so the route has diagonal transitions.

    # collect the traversal as runs of evenly spaced indices and offsets:
    # (start index, index step, count, start offset, offset step)
    runs = []

    for event, level, data in _traverse(tree, level):
        if event == _GAP:
            # all points of the gap at the current level
            gap_indices = data[0]
            if len(gap_indices) > 0:
                runs.append(
                    (gap_indices.start, gap_indices.step, len(gap_indices), level, 0)
                )
            continue

        level_indices = data
        level_length = len(level_indices) - 1

        # The ramps leave out the last point of the range: the following run starts
        # there at the new level.
        if event == _ENTER and level > 0 and level_length > 0:
            # start to end, level up
            runs.append(
                (
                    level_indices[0],
                    level_indices.step,
                    level_length,
                    level - 1,
                    1 / level_length,
                )
            )
        elif event == _EXIT and level == 0:
            # the final point of the route
            runs.append((level_indices[0], 1, 1, level, 0))
        elif event == _EXIT and level_length > 0:
            # start to end, level down
            runs.append(
                (
                    level_indices[0],
                    level_indices.step,
                    level_length,
                    level,
                    -1 / level_length,
                )
            )

    # expand all runs at once instead of element by element
    start, step, count, offset, offset_step = (np.array(c) for c in zip(*runs))

    # position of each element within its run
    k = np.arange(count.sum()) - np.repeat(np.cumsum(count) - count, count)

    indices = np.repeat(start, count) + k * np.repeat(step, count)
    offsets = np.repeat(offset, count) + k * np.repeat(offset_step, count)
    return indices, offsets


def tree_to_indices_and_offsets_basic(tree, level=0):
    # Returns only the corner points of the stitch route, as (index, level) pairs.
    # Consecutive points are meant to be connected by lines that the caller
    # subdivides itself (see variable_underlay). Compared to tree_to_indices_and_offsets,
    # the first and last gap of each level are folded into the diagonal lines to and
    # from the neighbouring child.
    indices = []
    offsets = []

    for event, level, data in _traverse(tree, level):
        if event == _ENTER:
            # the point where the walk at this level starts; for level > 0, the line
            # towards it is the diagonal move up from the previous level
            indices.append(data[-1])
            offsets.append(level)
        elif event == _EXIT:
            # the point where the walk at this level ends
            indices.append(data[0])
            offsets.append(level)
        else:
            # only the gap's end points, skipping the first and last gap of each level
            gap_indices, is_first, is_last = data
            if len(gap_indices) > 1 and not is_first and not is_last:
                indices.append(gap_indices[0])
                indices.append(gap_indices[-1])
                offsets.append(level)
                offsets.append(level)

    return indices, offsets
