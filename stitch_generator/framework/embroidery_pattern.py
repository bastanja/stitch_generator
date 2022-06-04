import numpy as np

from stitch_generator.framework.types import Rectangle


class EmbroideryPattern:
    def __init__(self):
        self.stitch_blocks = []
        self.colors = []
        self._block_offsets = []

    def add_stitches(self, coordinates, color=0x808080):
        assert len(coordinates) > 0, "Stitch coordinates are empty"
        self.stitch_blocks.append(np.array(coordinates))
        self.colors.append(color)
        self._block_offsets = np.add.accumulate([len(b) for b in self.stitch_blocks])

    def get_stitch(self, stitch_index):
        assert stitch_index >= 0, "Negative stitch index"
        assert len(self.stitch_blocks) > 0, "The EmbroideryPattern has no stitches"
        assert stitch_index < self.number_of_stitches, "stitch_index out of range"

        block_index = np.searchsorted(self._block_offsets, stitch_index + 1)
        if block_index > 0:
            stitch_index -= self._block_offsets[block_index - 1]
        block = self.stitch_blocks[block_index]
        stitch = block[stitch_index]
        return tuple(stitch)

    @property
    def number_of_stitches(self):
        if len(self._block_offsets) == 0:
            return 0
        return self._block_offsets[-1]


def bounding_rect(pattern: EmbroideryPattern) -> Rectangle:
    all_stitches = np.concatenate(pattern.stitch_blocks)
    min = np.min(all_stitches, axis=0)
    max = np.max(all_stitches, axis=0)
    return Rectangle(min[0], min[1], max[0], max[1])
