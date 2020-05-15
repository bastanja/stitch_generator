from pyembroidery import EmbPattern, write_vp3, write_svg, \
    CONTINGENCY_TIE_ON_THREE_SMALL, CONTINGENCY_TIE_OFF_THREE_SMALL

from stitch_generator.functions.embroidery_pattern import EmbroideryPattern


def to_pyembroidery(embroidery_pattern: EmbroideryPattern):
    scale_factor = 10  # convert from millimeters to embroidery file scale 1/10 mm
    result = EmbPattern()

    for i in range(len(embroidery_pattern.stitch_blocks)):
        scaled_stitches = embroidery_pattern.stitch_blocks[i] * scale_factor
        result.add_block(scaled_stitches.tolist(), embroidery_pattern.colors[i])

    return result


export_parameters = {"tie_on": CONTINGENCY_TIE_ON_THREE_SMALL, "tie_off": CONTINGENCY_TIE_OFF_THREE_SMALL}


def export_vp3(pattern: EmbroideryPattern, file_path: str):
    write_vp3(to_pyembroidery(pattern), file_path, export_parameters)


def export_svg(pattern: EmbroideryPattern, file_path: str):
    write_svg(to_pyembroidery(pattern), file_path)
