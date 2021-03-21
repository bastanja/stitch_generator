from types import SimpleNamespace

from stitch_generator.framework.cli import get_parser, write_pattern_to_file


class EmbroideryDesign:
    def __init__(self, name: str, parameters: dict):
        self.parameters = parameters
        self.name = name

    def validate(self, parameters):
        default_parameters = {k: v.value for k, v in self.parameters.items()}

        if parameters:
            update_parameters = {k: self.parameters[k].evaluate(v) for k, v in parameters.items() if
                                 k in self.parameters}
            default_parameters.update(update_parameters)
        return SimpleNamespace(**default_parameters)

    def cli(self):
        parser = get_parser(self.parameters)
        args = parser.parse_args()
        print(f"Exporting design {self.name} to file.")
        write_pattern_to_file(self, vars(args))
