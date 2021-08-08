import argparse

from stitch_generator.file_io.embroidery_export import export_vp3
from stitch_generator.framework.parameter import IntParameter, FloatParameter, BoolParameter


def get_parser(design_parameters: dict):
    parser = argparse.ArgumentParser(description='Create embroidery patterns.')

    for parameter_name, parameter in design_parameters.items():
        if _parameter_type_supported(parameter):
            parser.add_argument(f"--{parameter_name}",
                                default=parameter.value,
                                help=parameter.get_description(),
                                type=parameter.expected_type())

    return parser


def write_pattern_to_file(design, parameters):
    file_type = "vp3"
    pattern = design.get_pattern(parameters=parameters)
    export_vp3(pattern, f"{design.name}.{file_type}")


def _parameter_type_supported(parameter):
    if type(parameter) in (IntParameter, FloatParameter, BoolParameter):
        return True
    return False
