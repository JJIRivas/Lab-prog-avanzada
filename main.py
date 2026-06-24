from algoritmos import astar, bfs, dfs, ucs
from algoritmos.astar import cero
from escenarios import grafo as mod_grafo
from escenarios import laberinto as mod_laberinto

NOMBRES = {1: "BFS", 2: "DFS", 3: "UCS", 4: "A*"}
# Ambos lab y main tienen a mi lsp quejandose por possibly unbound, pero ya deberian estar definidas las variables para ese punto asi que


def seleccionar(prompt, opciones):
    while True:
        try:
            opcion = int(input(prompt))
            if opcion in opciones:
                return opcion
        except ValueError:
            pass


def main():
    print("1. Grafo\n2. Laberinto")
    escenario = seleccionar("Escenario: ", (1, 2))

    print("\nAlgoritmo:\n1. BFS\n2. DFS\n3. UCS\n4. A*")
    algoritmo = seleccionar("Algoritmo: ", (1, 2, 3, 4))

    if escenario == 1:
        nodos = list(mod_grafo.grafo.keys())
        print(f"\nNodos disponibles: {nodos}")

        inicio = input("Nodo inicial: ").strip().upper()
        while inicio not in nodos:
            print(f"Nodo inválido. Opciones: {nodos}")
            inicio = input("Nodo inicial: ").strip().upper()

        objetivo = input("Nodo objetivo: ").strip().upper()
        while objetivo not in nodos:
            print(f"Nodo inválido. Opciones: {nodos}")
            objetivo = input("Nodo objetivo: ").strip().upper()

        # BFS/DFS usan grafo sin pesos; UCS/A* usan grafo con pesos
        con_pesos = algoritmo in (3, 4)
        get_vecinos = (
            mod_grafo.get_vecinos_pesos if con_pesos else mod_grafo.get_vecinos_simple
        )

        match algoritmo:
            case 1:
                visitados, camino, costo = bfs.bbfs(inicio, objetivo, get_vecinos)
            case 2:
                visitados, camino, costo = dfs.ddfs(inicio, objetivo, get_vecinos)
            case 3:
                visitados, camino, costo = ucs.uucs(inicio, objetivo, get_vecinos)
            case 4:
                # Sin coordenadas espaciales heurística cero qyw equivale a UCS
                visitados, camino, costo = astar.aastar(
                    inicio, objetivo, get_vecinos, cero
                )

        nombre = NOMBRES[algoritmo]
        if camino:
            print(f"\n[{nombre}] Camino:   {' → '.join(camino)}")
            print(f"Costo: {costo}")
            print(f"Visitados: {visitados}")
        else:
            print(f"\n[{nombre}] No se encontró camino")

        mod_grafo.visualizar(visitados, camino, costo, nombre)

    elif escenario == 2:
        mod_laberinto.init(algoritmo)


if __name__ == "__main__":
    main()
