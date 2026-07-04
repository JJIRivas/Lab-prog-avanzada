from adts import incident


class parser:
    def __init__(self) -> None:
        pass

    def parseFile(self, filepath):
        return self.parse(filepath)

    def parse(self, data):

        for item in data:
            incident_id = item["id"]
            incident_ubicacion = item["ubicacion"]
            incident_prioridad = item["prioridad"]
            incident_tipo = item["tipo"]
            incident_timestamp = item["timestamp"]
            incident_estado = item["estado"]

            yield incident.incident(
                incident_id,
                incident_ubicacion,
                incident_prioridad,
                incident_tipo,
                incident_timestamp,
                incident_estado,
            )
