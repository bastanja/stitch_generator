from types import SimpleNamespace


class EmbroideryDesign:
    def __init__(self):
        pass


def parameter_evaluation(evaluation_parameters):
    def evaluation_function(parameters):
        default_parameters = {k: v.value for k, v in evaluation_parameters.items()}

        if parameters:
            update_parameters = {k: evaluation_parameters[k].evaluate(v) for k, v in parameters.items() if
                                 k in evaluation_parameters}
            default_parameters.update(update_parameters)
        return SimpleNamespace(**default_parameters)

    return evaluation_function
