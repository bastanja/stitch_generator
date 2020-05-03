class EmbroideryDesign:
    def __init__(self):
        self.parameters = {}

    def set_own_attributes(self):
        for name, param in self.parameters.items():
            setattr(self, name, param.value)

