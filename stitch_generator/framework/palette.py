import itertools

light = [
    0x148983,
    0x1873AC,
    0x8C5290,
    0x61A09C,
    0x5AD2F4,
]

dark = [
    0x0F6460,
    0x0F4668,
    0x543156,
    0x487673,
    0x0C8BAF,
]

combined = light + dark


def palette(colors=combined):
    return itertools.cycle(colors)
