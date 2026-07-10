from adts import emergencyCenter
from fileHandlers import baseParser


# Retorna los centros medicos del csv o json correspondiente. Ocupa yield para evitar crear nuevos objetos al enviar cada uno.
class centerParser(baseParser.parser):
    def parse(self, data):
        for item in data:
            yield emergencyCenter.emergencyCenter(
                item["id"],
                item["nombre"],
                item["ubicacion"],  # debe matchear un nodo del grafo
            )
