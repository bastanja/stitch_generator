def alignment_to_offset(relative_segment_length: float, offset: float, alignment: float):
    # Map alignment into the range of one segment
    alignment = alignment % relative_segment_length

    # Calculate the alignment position relative to one segment length
    relative_alignment = alignment / relative_segment_length

    return (offset + relative_alignment) % 1
