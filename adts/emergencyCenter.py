# Centros de emergencia.
class emergencyCenter:
    def __init__(self, id, nombre, ubicacion):
        self.id = id
        self.nombre = nombre
        self.ubicacion = ubicacion  # nodo del grafo. Deberia ser parte de roadNetwork

    def __repr__(self):
        return f"EmergencyCenter({self.nombre} @ {self.ubicacion})"
