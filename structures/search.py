import heapq
import math


# Nota: Se ocupa heapq para UCS/A*, ya que PHeah fue diseañada para incidentes.
# Deberia estar OK ya que la unica restriccion del enunciado era sobre tablas Hash.
class search:
    @staticmethod
    def bfs(grafo, inicio, destino) -> dict:
        inicio = grafo.normalizar(inicio)
        destino = grafo.normalizar(destino)

        cola = [inicio]
        visitados = [inicio]
        padres = {inicio: None}

        while cola:
            actual = cola.pop(0)
            if actual == destino:
                break
            for vecino, _peso in grafo.vecinos(actual):
                if vecino not in padres:
                    padres[vecino] = actual
                    visitados.append(vecino)
                    cola.append(vecino)

        return search._construirResultado(grafo, inicio, destino, padres, visitados)

    @staticmethod
    def ucs(grafo, inicio, destino) -> dict:
        inicio = grafo.normalizar(inicio)
        destino = grafo.normalizar(destino)

        frontera = [(0, inicio)]  # min-heap de costo_acumulado, nodo
        costos = {inicio: 0}
        padres = {inicio: None}
        visitados = []

        while frontera:
            costo_actual, actual = heapq.heappop(frontera)
            if actual in visitados:
                continue  # si ya se proceso este nodo con un costo mejor o igual
            visitados.append(actual)
            if actual == destino:
                break
            for vecino, peso in grafo.vecinos(actual):
                nuevo_costo = costo_actual + peso
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    padres[vecino] = actual
                    heapq.heappush(frontera, (nuevo_costo, vecino))

        return search._construirResultado(grafo, inicio, destino, padres, visitados)

    @staticmethod
    def aStar(grafo, inicio, destino, heuristica=None) -> dict:
        inicio = grafo.normalizar(inicio)
        destino = grafo.normalizar(destino)
        heuristica = heuristica or (lambda nodo: 0)

        frontera = [
            (heuristica(inicio), 0, inicio)
        ]  # prioridad con heuristica, costo real, nodo
        costos = {inicio: 0}
        padres = {inicio: None}
        visitados = []

        while frontera:
            _prioridad, costo_actual, actual = heapq.heappop(frontera)
            if actual in visitados:
                continue
            visitados.append(actual)
            if actual == destino:
                break
            for vecino, peso in grafo.vecinos(actual):
                nuevo_costo = costo_actual + peso
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    padres[vecino] = actual
                    prioridad = nuevo_costo + heuristica(vecino)
                    heapq.heappush(frontera, (prioridad, nuevo_costo, vecino))

        return search._construirResultado(grafo, inicio, destino, padres, visitados)

    # Intento de heuristica real basada en distancia para el tiempo.
    # Se considero una vel maxima de 120 y se ocupo para los calculos, evitando
    # que hubieran casos donde el estimado fuera menor al tiempo real. Siempre deberia
    # ser mayor o igual.
    @staticmethod
    def heuristicaHaversine(grafo, destino, velocidad_max_kmh=120):
        destino = grafo.normalizar(destino)
        coord_destino = grafo.coordenadas(destino)

        def h(nodo):
            coord_nodo = grafo.coordenadas(nodo)
            if coord_destino is None or coord_nodo is None:
                return 0
            distancia_km = search._haversine(coord_nodo, coord_destino)
            tiempo_estimado_min = (distancia_km / velocidad_max_kmh) * 60
            return tiempo_estimado_min

        return h

    # Distancia entre dos puntos sobre la superficie de una esfera. Sere honesto, esto es
    # codigo de internet. Funciona, pero no estoy seguro de la matematica.
    @staticmethod
    def _haversine(coord1, coord2):
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        R = 6371
        lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        return R * c

    # Construye el resultado (ruta) final ocupando el diccionario de padres en
    # reversa.
    @staticmethod
    def _construirResultado(grafo, inicio, destino, padres, visitados) -> dict:
        if destino not in padres:
            return {"ruta": None, "visitados": visitados, "costo_total": None}

        ruta = []
        nodo = destino
        while nodo is not None:
            ruta.append(nodo)
            nodo = padres[nodo]
        ruta.reverse()

        costo_total = 0
        for i in range(len(ruta) - 1):
            for vecino, peso in grafo.vecinos(ruta[i]):
                if vecino == ruta[i + 1]:
                    costo_total += peso
                    break

        return {"ruta": ruta, "visitados": visitados, "costo_total": costo_total}
