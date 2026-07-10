from datetime import datetime

from adts import incident
from fileHandlers import baseParser

FORMATO_TIMESTAMP = "%Y-%m-%d %H:%M:%S"


# Retorna los incidentes del csv o json correspondiente. Ocupa yield para evitar crear nuevos objetos al enviar cada uno- ademas, "formatea" las fechas para normalizar los datos de inmediato.
class incidentParser(baseParser.parser):
    def parse(self, data):
        for item in data:
            yield incident.incident(
                item["id"],
                item["ubicacion"],
                item["prioridad"],
                item["tipo"],
                datetime.strptime(item["timestamp"], FORMATO_TIMESTAMP),
                item["estado"],
            )
