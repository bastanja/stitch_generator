from types import SimpleNamespace

from stitch_generator.framework.cli import get_parser, write_pattern_to_file
from stitch_generator.framework.embroidery_pattern import EmbroideryPattern


class EmbroideryDesign:
    """
    An EmbroideryDesign creates EmbroideryPatterns based on input parameters.

    While an EmbroideryPattern is static and contains only stitch positions, an EmbroideryDesign can dynamically change
    based on parameters. For example a design may have parameters for size, stitch length, stitch density etc. Based on
    the values of these parameters, different EmbroideryPatterns can be created from the same EmbroideryDesign.
    """

    def __init__(self, name: str, parameters: dict):
        """
        Args:
            name: The name of the design. Used as filename when exporting the design as embroidery file.
            parameters: A dictionary that maps parameter names to parameters like FloatParameter, IntParameter etc.
                These parameters can be used in the get_pattern function of the EmbroideryDesign
        """
        self.parameters = parameters
        self.name = name

    def _validate(self, parameters):
        """
        Checks if the provided parameters have valid values, clamps them into the valid value ranges. Writes the
        validated parameters from a dict to a SimpleNamespace and returns it

        Args:
            parameters: a dictionary of parameters with names and values

        Returns:
            SimpleNamespace with variables that have the keys of the dictionary as name and the validated values of the
            variables as values
        """
        default_parameters = {k: v.value for k, v in self.parameters.items()}

        if parameters:
            update_parameters = {k: self.parameters[k].evaluate(v) for k, v in parameters.items() if
                                 k in self.parameters}
            default_parameters.update(update_parameters)
        return SimpleNamespace(**default_parameters)

    def _to_pattern(self, parameters: SimpleNamespace, pattern: EmbroideryPattern):
        """
        Fills the provided EmbroideryPattern with stitch blocks based on the parameters. Derived classes must implement
        this function.
        Args:
            parameters: The validated parameters of the design
            pattern: The pattern to add the stitches to
        """
        pass

    def get_pattern(self, parameters) -> EmbroideryPattern:
        """
        Validates the parameters and returns the EmbroideryPattern which is created with the parameters
        Args:
            parameters: A dictionary with parameter values.

        Returns:
            An EmbroideryPattern
        """
        validated_parameters = self._validate(parameters)
        pattern = EmbroideryPattern()

        self._to_pattern(validated_parameters, pattern)

        return pattern

    def cli(self):
        """
        Provides a command line interface for creating an embroidery file from the design. Reads command line arguments
        and passes them to the get_pattern function, writes the EmbroideryPattern to a file.
        """
        parser = get_parser(self.parameters)
        args = parser.parse_args()
        print(f"Exporting design {self.name} to {args.file_format} file.")
        write_pattern_to_file(self, vars(args), args.file_format)
