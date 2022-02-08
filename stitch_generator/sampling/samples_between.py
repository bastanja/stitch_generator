def samples_between(total_length, start_offset, end_offset, sampling_function):
    """
    Calls the sampling function on a segment between start_offset and end_offset
    Args:
        total_length: The total length of the shape that is sampled
        start_offset: the relative offset between 0 and 1 on the shape where the segment starts
        end_offset: the relative offset between 0 and 1 on the shape where the segment ends
        sampling_function: The sampling function to call for the segment

    Returns: samples between start_offset and end_offset
    """
    delta = end_offset - start_offset
    length = delta * total_length
    samples = sampling_function(length) * delta + start_offset
    return samples
