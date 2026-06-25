import heapq


def uucs(inicio, objetivo, get_vecinos):

    contador = 0  # Desempate cuando dos nodos tienen el mismo costo
    heap = [(0, contador, inicio, [inicio])]
    visitados = []
    vistos = {}

    while heap:
        costo, _, nodo, camino = heapq.heappop(heap)

        if nodo in vistos:
            continue

        vistos[nodo] = costo
        visitados.append(nodo)

        if nodo == objetivo:
            return visitados, camino, costo

        for vecino, peso in get_vecinos(nodo):
            if vecino not in vistos:
                contador += 1
                heapq.heappush(
                    heap, (costo + peso, contador, vecino, camino + [vecino])
                )

    return visitados, [], None
