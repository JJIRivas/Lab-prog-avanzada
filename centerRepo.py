from fileHandlers import centerParser as cp


# Objeto que tiene los centros medicos.
class EmergencyCenterRepo:
    def __init__(self):
        self.centros = []
        self.parser = cp.centerParser()

    def load(self, filepath):
        for centro in self.parser.parseFile(filepath):
            self.centros.append(centro)
