def subdivide_between(total_length, start_offset, end_offset, subdivision_function):
    """
    Calls the subdivision function on a segment between start_offset and end_offset
    Args:
        total_length: The total length of the shape that is subdivided
        start_offset: the relative offset between 0 and 1 on the shape where the segment starts
        end_offset: the relative offset between 0 and 1 on the shape where the segment ends
        subdivision_function: The subdivision function to call for the segment

    Returns: values between start_offset and end_offset
    """
    delta = end_offset - start_offset
    length = delta * total_length
    return subdivision_function(length) * delta + start_offset
