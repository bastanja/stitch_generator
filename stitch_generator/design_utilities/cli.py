import argparse

from stitch_generator.design_utilities.parameter import IntParameter, FloatParameter, BoolParameter
from stitch_generator.file_io.embroidery_export import export_vp3


def get_parser(design_parameters: dict):
    parser = argparse.ArgumentParser(description='Create embroidery patterns.')

    for parameter_name, parameter in design_parameters.items():
        if parameter_type_supported(parameter):
            parser.add_argument(f"--{parameter_name}",
                                default=parameter.value,
                                help=parameter.get_description(),
                                type=parameter.expected_type())

    return parser


def parameter_type_supported(parameter):
    if type(parameter) in (IntParameter, FloatParameter, BoolParameter):
        return True
    return False


def write_pattern_to_file(design, parameters, filename_base):
    file_type = "vp3"
    pattern = design.get_pattern(vars(parameters))
    export_vp3(pattern, f"{filename_base}.{file_type}")
