from fileHandlers import baseParser


# Retorna los caminos y pesos (si tiene) del csv o json correspondiente. Ocupa yield para evitar crear nuevos objetos al enviar cada uno.
class edgeParser(baseParser.parser):
    def parse(self, data):
        for item in data:
            yield (item["origen"], item["destino"], float(item["peso"]))
