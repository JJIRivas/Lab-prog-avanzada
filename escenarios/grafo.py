import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

grafo = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": ["H"],
    "E": ["I", "J"],
    "F": ["K"],
    "G": [],
    "H": [],
    "I": [],
    "J": [],
    "K": [],
}

grafo2 = {
    "A": {"B": 2, "C": 5},
    "B": {"D": 4, "E": 1},
    "C": {"F": 2, "G": 6},
    "D": {"H": 3},
    "E": {"I": 2, "J": 7},
    "F": {"K": 1},
    "G": {},
    "H": {},
    "I": {},
    "J": {},
    "K": {},
}

posiciones = {
    "A": (4.0, 4.0),
    "B": (2.0, 3.0),
    "C": (6.0, 3.0),
    "D": (1.0, 2.0),
    "E": (3.0, 2.0),
    "F": (5.0, 2.0),
    "G": (7.0, 2.0),
    "H": (1.0, 1.0),
    "I": (2.5, 1.0),
    "J": (3.5, 1.0),
    "K": (5.0, 1.0),
}


def get_vecinos_simple(nodo):
    # BFS y DFS costo uniforme 1
    return [(vecino, 1) for vecino in grafo[nodo]]


def get_vecinos_pesos(nodo):
    # UCS y A* con pesos
    return [(vecino, costo) for vecino, costo in grafo2[nodo].items()]


def visualizar(visitados=None, camino=None, costo=None, nombre_algoritmo=""):
    fig, ax = plt.subplots(figsize=(10, 7))

    visitados_set = set(visitados) if visitados else set()
    camino_set = set(camino) if camino else set()
    camino_pares = set(zip(camino, camino[1:])) if camino else set()

    # Aristas
    for nodo, vecinos in grafo2.items():
        x1, y1 = posiciones[nodo]
        for vecino, peso in vecinos.items():
            x2, y2 = posiciones[vecino]

            en_camino = (nodo, vecino) in camino_pares
            color = "#FFD700" if en_camino else "#BBBBBB"
            lw = 4 if en_camino else 1.5

            ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=1)

            # Etiquetas peso
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my,
                str(peso),
                fontsize=9,
                ha="center",
                va="center",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1),
            )

    for nodo, (x, y) in posiciones.items():
        if camino and nodo == camino[0]:
            color, tc = "#00C851", "white"  # inicio
        elif camino and nodo == camino[-1]:
            color, tc = "#FF4444", "white"  # objetivo
        elif nodo in camino_set:
            color, tc = "#FFD700", "black"  # camino
        elif nodo in visitados_set:
            color, tc = "#87CEEB", "black"  # visitado
        else:
            color, tc = "white", "black"  # no visitado

        circle = mpatches.Circle(
            (x, y), 0.3, color=color, ec="#333333", linewidth=2, zorder=3
        )
        ax.add_patch(circle)
        ax.text(
            x,
            y,
            nodo,
            ha="center",
            va="center",
            fontsize=13,
            fontweight="bold",
            color=tc,
            zorder=4,
        )

    titulo = nombre_algoritmo
    if camino:
        titulo += f"Costo: {costo}  |  Visitados: {visitados}"
    elif visitados is not None:
        titulo += "Sin camino"
    ax.set_title(titulo, fontsize=11, pad=12)

    leyenda = [
        mpatches.Patch(color="#00C851", label="Inicio"),
        mpatches.Patch(color="#FF4444", label="Objetivo"),
        mpatches.Patch(color="#FFD700", label="Camino"),
        mpatches.Patch(color="#87CEEB", label="Visitado"),
        mpatches.Patch(color="white", label="No visitado", ec="#333333"),
    ]
    ax.legend(handles=leyenda, loc="upper left", fontsize=9)

    ax.set_xlim(0, 8)
    ax.set_ylim(0.3, 4.8)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.show()
