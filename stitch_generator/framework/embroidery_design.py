from types import SimpleNamespace
from typing import Iterable

from stitch_generator.framework.cli import get_parser, write_pattern_to_file
from stitch_generator.framework.embroidery_pattern import EmbroideryPattern
from stitch_generator.framework.palette import palette


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
        default_parameters = {k: v.value for k, v in self.parameters.items()}

        if parameters:
            update_parameters = {k: self.parameters[k].evaluate(v) for k, v in parameters.items() if
                                 k in self.parameters}
            default_parameters.update(update_parameters)
        return SimpleNamespace(**default_parameters)

    def _to_pattern(self, parameters: SimpleNamespace, pattern: EmbroideryPattern, colors: Iterable):
        pass

    def get_pattern(self, parameters):
        validated_parameters = self._validate(parameters)
        pattern = EmbroideryPattern()

        self._to_pattern(validated_parameters, pattern, palette())

        return pattern

    def cli(self):
        parser = get_parser(self.parameters)
        args = parser.parse_args()
        print(f"Exporting design {self.name} to file.")
        write_pattern_to_file(self, vars(args))
