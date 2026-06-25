from collections import deque


def bbfs(inicio, objetivo, get_vecinos):
    cola = deque([(inicio, [inicio])])
    visitados = []
    vistos = {inicio}

    while cola:
        nodo, camino = cola.popleft()
        visitados.append(nodo)

        if nodo == objetivo:
            return visitados, camino, len(camino) - 1

        for vecino, _ in get_vecinos(nodo):
            if vecino not in vistos:
                vistos.add(vecino)
                cola.append((vecino, camino + [vecino]))

    return visitados, [], None
