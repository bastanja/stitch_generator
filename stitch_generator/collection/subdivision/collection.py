from stitch_generator.collection.subdivision.subdivision_with_varying_offset import subdivision_with_triangle_offset, \
    subdivision_with_arc_offset, subdivision_with_wave_offset
from stitch_generator.collection.subdivision.subdivison_with_varying_alignment import \
    subdivision_with_triangle_alignment
from stitch_generator.collection.subdivision.tatami import tatami_3_1, tatami_4_2
from stitch_generator.subdivision.subdivision_modifiers import free_start, free_end, alternate_direction


def free_start_end(subdivision_function):
    return free_start(1, free_end(1, subdivision_function))


def subdivision_functions():
    yield tatami_3_1(segment_length=4)
    yield tatami_4_2(segment_length=3)
    yield free_start_end(alternate_direction(subdivision_with_triangle_offset(segment_length=3.5, steps=30)))
    yield free_start_end(subdivision_with_arc_offset(segment_length=3, steps=30, function_range=(0.75, 0.25)))
    yield free_start_end(subdivision_with_wave_offset(segment_length=3, steps=60, function_range=(0.2, 0.8)))
    yield free_start_end(subdivision_with_triangle_offset(segment_length=3, steps=40))
    yield free_start_end(subdivision_with_triangle_alignment(segment_length=3, steps=30, function_range=(0.35, 0.65)))
