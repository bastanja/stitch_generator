from stitch_generator.functions.functions_2d import line
from stitch_generator.functions.sample import sample_by_length


def running_stitch(function, stitch_length: float, include_last: bool):
    assert stitch_length > 0, "Stitch length must be greater than zero"
    return sample_by_length(function, stitch_length=stitch_length, include_endpoint=include_last)


def running_stitch_line(p1, p2, stitch_length: float, include_last: bool):
    function = line(p1, p2)
    return running_stitch(function=function, stitch_length=stitch_length, include_last=include_last)
