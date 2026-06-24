import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from algoritmos import astar, bfs, dfs, ucs
from algoritmos.astar import manhattan

inicio = None
objetivo = None
algoritmo_seleccionado = None
fig, ax = plt.subplots(figsize=(7, 7))

laberinto = [
    [1, 1, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
]

NOMBRES = {1: "BFS", 2: "DFS", 3: "UCS", 4: "A*"}

# 0=libre, 1=pared, 2=visitado, 3=camino
CMAP = mcolors.ListedColormap(["white", "#2C2C2C", "#87CEEB", "#FFD700"])
NORM = mcolors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], CMAP.N)


def get_vecinos(pos):

    fila, col = pos
    vecinos = []
    for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nf, nc = fila + df, col + dc
        if 0 <= nf < len(laberinto) and 0 <= nc < len(laberinto[0]):
            if laberinto[nf][nc] == 0:
                vecinos.append(((nf, nc), 1))
    return vecinos


def init(algoritmo):
    global algoritmo_seleccionado
    algoritmo_seleccionado = algoritmo
    fig.canvas.mpl_connect("button_press_event", onclick)
    dibujar()
    plt.show()


def ejecutar():
    if not inicio:
        print("Selecciona un inicio (click izquierdo)")
        return
    if not objetivo:
        print("Selecciona un objetivo (click derecho)")
        return

    match algoritmo_seleccionado:
        case 1:
            visitados, camino, costo = bfs.bbfs(inicio, objetivo, get_vecinos)
        case 2:
            visitados, camino, costo = dfs.ddfs(inicio, objetivo, get_vecinos)
        case 3:
            visitados, camino, costo = ucs.uucs(inicio, objetivo, get_vecinos)
        case 4:
            visitados, camino, costo = astar.aastar(
                inicio, objetivo, get_vecinos, manhattan
            )

    nombre = NOMBRES[algoritmo_seleccionado]
    if camino:
        print(f"[{nombre}] Costo: {costo} | Visitados: {len(visitados)}")
    else:
        print(f"[{nombre}] Sin camino")

    dibujar(visitados, camino)


def dibujar(visitados=None, camino=None):
    ax.clear()

    color_matrix = np.array(laberinto, dtype=float)

    if visitados:
        for fila, col in visitados:
            color_matrix[fila][col] = 2

    if camino:
        for fila, col in camino:
            color_matrix[fila][col] = 3

    ax.imshow(color_matrix, cmap=CMAP, norm=NORM)

    if inicio:
        ax.scatter(inicio[1], inicio[0], color="#00C851", s=250, zorder=5, marker="o")
    if objetivo:
        ax.scatter(
            objetivo[1], objetivo[0], color="#FF4444", s=250, zorder=5, marker="*"
        )

    nombre = NOMBRES.get(algoritmo_seleccionado, "")
    if camino is not None:
        titulo = (
            f"{nombre} Costo: {len(camino) - 1} Visitados: {len(visitados)}"
            if camino
            else f"{nombre} Sin camino"
        )
    else:
        titulo = f"{nombre} Izq: inicio Der: objetivo Medio: ejecutar"
    ax.set_title(titulo, fontsize=10)

    leyenda = [
        mpatches.Patch(color="#00C851", label="Inicio"),
        mpatches.Patch(color="#FF4444", label="Objetivo"),
        mpatches.Patch(color="#87CEEB", label="Visitado"),
        mpatches.Patch(color="#FFD700", label="Camino"),
        mpatches.Patch(color="#2C2C2C", label="Pared"),
    ]
    ax.legend(handles=leyenda, loc="upper right", fontsize=8)

    plt.draw()


def onclick(event):
    global inicio, objetivo

    if event.xdata is None or event.ydata is None:
        return

    fila = int(round(event.ydata))
    columna = int(round(event.xdata))

    if not (0 <= fila < len(laberinto) and 0 <= columna < len(laberinto[0])):
        return

    if event.button == 2:
        ejecutar()
        return

    if laberinto[fila][columna] == 1:
        print("Celda bloqueada")
        return

    if event.button == 1:
        inicio = (fila, columna)
        print("Inicio:", inicio)
    elif event.button == 3:
        objetivo = (fila, columna)
        print("Objetivo:", objetivo)

    dibujar()
