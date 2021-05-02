from pyembroidery import EmbPattern, write_vp3, write_svg, CONTINGENCY_TIE_ON_THREE_SMALL, \
    CONTINGENCY_TIE_OFF_THREE_SMALL

from stitch_generator.framework.embroidery_pattern import EmbroideryPattern


def to_pyembroidery(embroidery_pattern: EmbroideryPattern, scale_factor: float = 10):
    result = EmbPattern()

    for i in range(len(embroidery_pattern.stitch_blocks)):
        scaled_stitches = embroidery_pattern.stitch_blocks[i] * scale_factor
        result.add_block(scaled_stitches.tolist(), embroidery_pattern.colors[i])

    return result


export_parameters = {"tie_on": CONTINGENCY_TIE_ON_THREE_SMALL, "tie_off": CONTINGENCY_TIE_OFF_THREE_SMALL}


def export_vp3(pattern: EmbroideryPattern, file_path: str):
    scale_factor = 10  # convert from millimeters to embroidery file scale 1/10 mm
    write_vp3(to_pyembroidery(pattern, scale_factor=scale_factor), file_path, export_parameters)


def export_pattern(pattern: EmbroideryPattern, file_path: str):
    """
    Exports an EmbroideryPattern to a file
    Args:
        pattern: The EmbroideryPattern to write
        file_path: The file path including the file extension. The extension defines the written file format.
    """
    scale_factor = 10  # convert from millimeters to embroidery file scale 1/10 mm
    pyembroidery_pattern = to_pyembroidery(pattern, scale_factor=10)
    EmbPattern.static_write(pyembroidery_pattern, file_path, export_parameters)


def writable_formats():
    formats = [f for f in EmbPattern.supported_formats() if "writer" in f]
    return [{f["extension"]: f["description"]} for f in formats]


def export_svg(pattern: EmbroideryPattern, file_path: str):
    write_svg(to_pyembroidery(pattern, scale_factor=1), file_path)
