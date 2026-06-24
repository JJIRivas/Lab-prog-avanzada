def ddfs(inicio, objetivo, get_vecinos):

    pila = [(inicio, [inicio])]
    visitados = []
    vistos = set()  # Se marca al desapilar para el recorrido

    while pila:
        nodo, camino = pila.pop()

        if nodo in vistos:
            continue

        vistos.add(nodo)
        visitados.append(nodo)

        if nodo == objetivo:
            return visitados, camino, len(camino) - 1

        for vecino, _ in get_vecinos(nodo):
            if vecino not in vistos:
                pila.append((vecino, camino + [vecino]))

    return visitados, [], None
