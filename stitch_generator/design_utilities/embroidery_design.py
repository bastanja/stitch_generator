from types import SimpleNamespace


class EmbroideryDesign:
    def __init__(self, parameters: dict):
        self.parameters = parameters

    def validate(self, parameters):
        default_parameters = {k: v.value for k, v in self.parameters.items()}

        if parameters:
            update_parameters = {k: self.parameters[k].evaluate(v) for k, v in parameters.items() if
                                 k in self.parameters}
            default_parameters.update(update_parameters)
        return SimpleNamespace(**default_parameters)
