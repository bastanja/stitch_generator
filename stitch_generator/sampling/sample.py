import numpy as np

from stitch_generator.sampling.sample_by_number import sample_by_number


def alignment_to_offset(relative_segment_length: float, offset: float, alignment: float):
    # Map alignment into the range of one segment
    alignment = alignment % relative_segment_length

    # Calculate the alignment position relative to one segment length
    relative_alignment = alignment / relative_segment_length

    return (offset + relative_alignment) % 1


def sample(total_length: float,
           segment_length: float,
           alignment: float,
           offset: float):
    if total_length == 0 or segment_length == 0:
        return sample_by_number(1)
    step_size = segment_length / total_length
    step_offset = alignment_to_offset(step_size, offset, alignment) * step_size
    return np.arange(start=step_offset, step=step_size, stop=1)
