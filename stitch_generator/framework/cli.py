import argparse

from stitch_generator.file_io.embroidery_export import export_pattern
from stitch_generator.framework.parameter import IntParameter, FloatParameter, BoolParameter


def get_parser(design_parameters: dict):
    parser = argparse.ArgumentParser(description='Create embroidery patterns.')

    for parameter_name, parameter in design_parameters.items():
        if _parameter_type_supported(parameter):
            parser.add_argument(f"--{parameter_name}",
                                default=parameter.value,
                                help=parameter.get_description(),
                                type=parameter.expected_type())

    parser.add_argument("--file_format", default="dst", help="Embroidery file format", type=str)

    return parser


def write_pattern_to_file(design, parameters, file_format):
    pattern = design.get_pattern(parameters=parameters)
    export_pattern(pattern, f"{design.name}.{file_format}")


def _parameter_type_supported(parameter):
    """
    Not all parameter types from stitch_generator.framework.parameter are supported in the command line interface.
    This function checks if a parameter is supported.

    Args:
        parameter: An EmbroideryDesign parameter

    Returns:
        Returns true if the parameter is a supported type (int, float, bool) and false if it is a type that is
        not supported via command line (ramp parameter)
    """

    if type(parameter) in (IntParameter, FloatParameter, BoolParameter):
        return True
    return False
