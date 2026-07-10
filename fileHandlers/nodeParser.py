from fileHandlers import baseParser


# Retorna los nodos (ubicacion incidentes y/o centros) del csv o json correspondiente. Ocupa yield para evitar crear nuevos objetos al enviar cada uno.
class nodeParser(baseParser.parser):
    def parse(self, data):
        for item in data:
            yield (item["nodo"], float(item["lat"]), float(item["lon"]))
