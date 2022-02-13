from stitch_generator.collection.sampling.sampling_with_alignment_function import triangle_alignment_sampling
from stitch_generator.collection.sampling.sampling_with_offset_function import triangle_offset_sampling, \
    arc_offset_sampling, wave_offset_sampling
from stitch_generator.collection.sampling.tatami_sampling import tatami_3_1, tatami_4_2
from stitch_generator.sampling.sampling_modifiers import free_start, free_end, alternate_direction


def free_start_end(sampling_function):
    return free_start(1, free_end(1, sampling_function))


def sampling_functions():
    yield tatami_3_1(segment_length=4)
    yield tatami_4_2(segment_length=3)
    yield free_start_end(alternate_direction(triangle_offset_sampling(segment_length=3.5, steps=30)))
    yield free_start_end(arc_offset_sampling(segment_length=3, steps=30, function_range=(0.75, 0.25)))
    yield free_start_end(wave_offset_sampling(segment_length=3, steps=60, function_range=(0.2, 0.8)))
    yield free_start_end(triangle_offset_sampling(segment_length=3, steps=40))
    yield free_start_end(triangle_alignment_sampling(segment_length=3, steps=30, function_range=(0.35, 0.65)))
