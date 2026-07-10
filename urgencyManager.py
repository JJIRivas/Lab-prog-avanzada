from typing import Optional

from structures import search as s


# Clase de "alto nivel" por decirlo de una manera. Sirve para manejar distintas funciones de repos y estructuras
# de manera mas facil y concisa. Actualmente define el algoritmo a ocupar para la busqueda. Default es astar.
class urgencyManager:
    def __init__(self, incident_repo, road_network, centros):
        self.incident_repo = incident_repo
        self.road_network = road_network
        self.centros = centros

    def centroMasCercano(self, incidente, algoritmo="astar") -> Optional[dict]:
        mejor = None

        for centro in self.centros:
            resultado = self._buscarRuta(
                centro.ubicacion, incidente.ubicacion, algoritmo
            )
            if resultado["ruta"] is None:
                continue

            if mejor is None or resultado["costo_total"] < mejor["costo_total"]:
                mejor = {
                    "centro": centro,
                    "ruta": resultado["ruta"],
                    "costo_total": resultado["costo_total"],
                    "nodos_visitados": resultado["visitados"],
                }

        return mejor

    def _buscarRuta(self, inicio, destino, algoritmo) -> dict:
        grafo = self.road_network.grafo

        if algoritmo == "bfs":
            return s.search.bfs(grafo, inicio, destino)
        elif algoritmo == "ucs":
            return s.search.ucs(grafo, inicio, destino)
        elif algoritmo == "astar":
            heuristica = s.search.heuristicaHaversine(grafo, destino)
            return s.search.aStar(grafo, inicio, destino, heuristica)
        else:
            raise ValueError(f"Algoritmo no soportado: {algoritmo}")

    def atenderSiguiente(self, algoritmo="astar") -> Optional[dict]:
        incidente = self.incident_repo.priority_queue.extractUrgent()
        if incidente is None:
            return None

        incidente.estado = "en_atencion"
        mejor = self.centroMasCercano(incidente, algoritmo)

        if mejor is None:
            return {
                "incidente": incidente,
                "centro": None,
                "ruta": None,
                "costo_total": None,
                "mensaje": "No se encontró ruta desde ningún centro disponible.",
            }

        return {
            "incidente": incidente,
            "centro": mejor["centro"],
            "ruta": mejor["ruta"],
            "costo_total": mejor["costo_total"],
            "nodos_visitados": mejor["nodos_visitados"],
        }
