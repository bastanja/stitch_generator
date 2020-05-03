import numpy as np


class EmbroideryPattern:
    def __init__(self):
        self.stitch_blocks = []
        self.colors = []
        self.block_offsets = []

    def add_stitches(self, coordinates, color=0x808080):
        assert len(coordinates) > 0, "Stitch coordinates are empty"
        self.stitch_blocks.append(np.array(coordinates))
        self.colors.append(color)
        self.block_offsets = np.add.accumulate([len(b) for b in self.stitch_blocks])

    def get_stitch(self, stitch_index):
        assert stitch_index >= 0, "Negative stitch index"
        assert len(self.stitch_blocks) > 0, "The EmbroideryPattern has no stitches"
        assert stitch_index < self.number_of_stitches, "stitch_index out of range"

        block_index = np.searchsorted(self.block_offsets, stitch_index + 1)
        if block_index > 0:
            stitch_index -= self.block_offsets[block_index - 1]
        block = self.stitch_blocks[block_index]
        stitch = block[stitch_index]
        return tuple(stitch)

    @property
    def number_of_stitches(self):
        if len(self.block_offsets) == 0:
            return 0
        return self.block_offsets[-1]