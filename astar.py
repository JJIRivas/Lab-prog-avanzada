import heapq


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Para distrib uniformes
def cero(a, b):
    return 0


def aastar(inicio, objetivo, get_vecinos, heuristica):
    contador = 0
    h0 = heuristica(inicio, objetivo)
    heap = [(h0, 0, contador, inicio, [inicio])]
    visitados = []
    vistos = {}

    while heap:
        f, g, _, nodo, camino = heapq.heappop(heap)

        if nodo in vistos:
            continue

        vistos[nodo] = g
        visitados.append(nodo)

        if nodo == objetivo:
            return visitados, camino, g

        for vecino, peso in get_vecinos(nodo):
            if vecino not in vistos:
                g_nuevo = g + peso
                f_nuevo = g_nuevo + heuristica(vecino, objetivo)
                contador += 1
                heapq.heappush(
                    heap, (f_nuevo, g_nuevo, contador, vecino, camino + [vecino])
                )

    return visitados, [], None
