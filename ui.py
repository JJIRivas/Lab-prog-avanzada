import math
import random
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt

# Mi IDE/LSP se queja por no encontrar NavigationToolbar2Tk, aunque esta
# existe y es ocupada correctamente. Si por alguna razon al ver el codigo aparace igual esto- deberia poder ignorarse. Al correr se muestra correctamente.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from structures import sorter as srt

# Clase que maneja la mayoria de las cosas relacionadas con UI.
# Deberia porblablement refractorizar a otros archivos pero para un "prototipo" creo que esta OK.


class mainView(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="lightblue", width=400, height=300, **kwargs)
        self.grid_propagate(False)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.ax.set_title("Red vial")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    # Parte que contiene el grafico de matplotlib para representar los caminos. Codigo es mayormente obtenido en linea ya que
    # no soy tan familiar con la libreria.
    def dibujarGrafo(self, grafo, ruta=None):
        self.ax.clear()

        nodos = grafo.obtenerNodos()
        if not nodos:
            self.canvas.draw()
            return

        posiciones = self._calcularPosiciones(grafo)

        for origen, destino, _peso in grafo.obtenerAristas():
            x0, y0 = posiciones[origen]
            x1, y1 = posiciones[destino]
            self.ax.plot([x0, x1], [y0, y1], color="lightgray", linewidth=1, zorder=1)

        if ruta:
            for i in range(len(ruta) - 1):
                x0, y0 = posiciones[ruta[i]]
                x1, y1 = posiciones[ruta[i + 1]]
                self.ax.plot([x0, x1], [y0, y1], color="red", linewidth=2.5, zorder=2)

        xs = [p[0] for p in posiciones.values()]
        ys = [p[1] for p in posiciones.values()]
        self.ax.scatter(xs, ys, color="steelblue", s=40, zorder=3)

        for nodo, (x, y) in posiciones.items():
            self.ax.annotate(
                nodo, (x, y), fontsize=6, xytext=(3, 3), textcoords="offset points"
            )

        self.ax.set_title("Red vial")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def _calcularPosiciones(self, grafo):
        nodos = grafo.obtenerNodos()
        tiene_coords_completas = all(grafo.coordenadas(n) is not None for n in nodos)

        if tiene_coords_completas:
            return {
                n: (grafo.coordenadas(n)[1], grafo.coordenadas(n)[0]) for n in nodos
            }  # lon, lat

        return self._springLayout(grafo, nodos)

    @staticmethod
    def _springLayout(grafo, nodos, iteraciones=50):
        n = len(nodos)
        k = 1.0 / math.sqrt(n)
        pos = {nodo: (random.uniform(0, 1), random.uniform(0, 1)) for nodo in nodos}
        aristas = [(o, d) for o, d, _ in grafo.obtenerAristas()]

        for _ in range(iteraciones):
            disp = {nodo: [0.0, 0.0] for nodo in nodos}

            for i, u in enumerate(nodos):
                for v in nodos[i + 1 :]:
                    dx, dy = pos[u][0] - pos[v][0], pos[u][1] - pos[v][1]
                    dist = math.hypot(dx, dy) or 0.01
                    fuerza = k * k / dist
                    disp[u][0] += (dx / dist) * fuerza
                    disp[u][1] += (dy / dist) * fuerza
                    disp[v][0] -= (dx / dist) * fuerza
                    disp[v][1] -= (dy / dist) * fuerza

            for u, v in aristas:
                dx, dy = pos[u][0] - pos[v][0], pos[u][1] - pos[v][1]
                dist = math.hypot(dx, dy) or 0.01
                fuerza = dist * dist / k
                disp[u][0] -= (dx / dist) * fuerza
                disp[u][1] -= (dy / dist) * fuerza
                disp[v][0] += (dx / dist) * fuerza
                disp[v][1] += (dy / dist) * fuerza

            for nodo in nodos:
                dx, dy = disp[nodo]
                despl = math.hypot(dx, dy) or 0.01
                pos[nodo] = (
                    pos[nodo][0] + (dx / despl) * min(despl, 0.1),
                    pos[nodo][1] + (dy / despl) * min(despl, 0.1),
                )

        return pos


# Contiene informacion sobre el camino relacionado con el incidente actual.
class BottomInfo(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="lightcyan", width=1030, height=100, **kwargs)
        self.grid_propagate(False)

        self.incidenteId = tk.StringVar(value="-")
        self.centroNombre = tk.StringVar(value="-")
        self.visitas = tk.IntVar(value=0)
        self.distancia = tk.DoubleVar(value=0.0)
        self.costo = tk.DoubleVar(value=0.0)

        stats = [
            ("Incidente:", self.incidenteId),
            ("Centro asignado:", self.centroNombre),
            ("N° Caminos considerados:", self.visitas),
            ("Distancia total:", self.distancia),
            ("Costo acumulado:", self.costo),
        ]

        for i, (texto, var) in enumerate(stats):
            frame = tk.Frame(self)
            frame.grid(row=0, column=i, padx=15, pady=10)
            ttk.Label(frame, text=texto).pack(side="left")
            ttk.Label(frame, textvariable=var).pack(side="left")

    def actualizar(self, incidente_id, centro_nombre, num_visitados, costo_total):
        self.incidenteId.set(str(incidente_id))
        self.centroNombre.set(str(centro_nombre))
        self.visitas.set(num_visitados)
        self.distancia.set(round(costo_total, 2))
        self.costo.set(round(costo_total, 2))

    def limpiar(self, mensaje="-"):
        self.incidenteId.set(mensaje)
        self.centroNombre.set("-")
        self.visitas.set(0)
        self.distancia.set(0.0)
        self.costo.set(0.0)


# Contiene los botones para que el programa funcione en base a lo que seleccione el usuario.
# Cargar los datos, ver historial, etc.
class Sidebar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="lightcyan", width=250, height=520, **kwargs)
        self.grid_propagate(False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(tuple(range(8)), weight=1)
        self.rowconfigure(8, weight=10)

        self.btnImportLugares = ttk.Button(self, text="1) Cargar Puntos de la Red")
        self.btnImportLugares.grid(row=0, column=0, pady=5)

        self.btnImportCaminos = ttk.Button(self, text="2) Cargar Calles")
        self.btnImportCaminos.grid(row=1, column=0, pady=5)

        self.btnImportarCentros = ttk.Button(
            self, text="3) Cargar Centros de Emergencia"
        )
        self.btnImportarCentros.grid(row=2, column=0, pady=5)

        self.btnImportIncicentes = ttk.Button(self, text="4) Cargar Incidentes")
        self.btnImportIncicentes.grid(row=3, column=0, pady=5)

        self.btnIncidentNuev = ttk.Button(self, text="Reportar Incidente")
        self.btnIncidentNuev.grid(row=4, column=0, pady=5)

        self.btnAtender = ttk.Button(self, text="Atender Siguiente")
        self.btnAtender.grid(row=5, column=0, pady=5)

        self.btnAuto = ttk.Button(self, text="Iniciar Modo Automático")
        self.btnAuto.grid(row=6, column=0, pady=5)

        self.btnHistorial = ttk.Button(self, text="Ver Historial")
        self.btnHistorial.grid(row=7, column=0, pady=5)


# Ventana para añadir un incidente de manera manual
class AddIncidentDialog(tk.Toplevel):
    TIPOS = [
        "incendio",
        "accidente vehicular",
        "inundacion",
        "robo",
        "emergencia medica",
        "derrumbe",
        "fuga de gas",
    ]

    def __init__(self, parent, on_submit):
        super().__init__(parent)
        self.title("Reportar Incidente")
        self.geometry("320x320")
        self.onSubmit = on_submit
        self.resizable(False, False)

        self.idVar = tk.StringVar()
        self.ubiVar = tk.StringVar()
        self.prioriVar = tk.IntVar(value=3)
        self.tipoVar = tk.StringVar()

        ttk.Label(self, text="ID:").pack(pady=(15, 0))
        ttk.Entry(self, textvariable=self.idVar).pack()

        ttk.Label(self, text="Ubicación (nodo de la red):").pack(pady=(10, 0))
        ttk.Entry(self, textvariable=self.ubiVar).pack()

        ttk.Label(self, text="Prioridad (1 a 5):").pack(pady=(10, 0))
        ttk.Spinbox(self, from_=1, to=5, textvariable=self.prioriVar, width=5).pack()

        ttk.Label(self, text="Tipo:").pack(pady=(10, 0))
        ttk.Combobox(
            self, textvariable=self.tipoVar, values=self.TIPOS, state="readonly"
        ).pack()

        ttk.Button(self, text="Reportar", command=self._enviar).pack(pady=20)

    def _enviar(self):
        if (
            not self.idVar.get().strip()
            or not self.ubiVar.get().strip()
            or not self.tipoVar.get()
        ):
            messagebox.showerror(
                "Faltan datos", "Completá todos los campos antes de reportar."
            )
            return

        self.onSubmit(
            self.idVar.get().strip(),
            self.ubiVar.get().strip(),
            self.prioriVar.get(),
            self.tipoVar.get(),
        )
        self.destroy()


class HistoryWindow(tk.Toplevel):
    OPCIONES = ["Más antiguos", "Más críticos", "Zonas con más incidentes"]

    def __init__(self, parent, incidentes_provider):
        super().__init__(parent)
        self.title("Historial de Incidentes")
        self.geometry("700x450")
        self.incidentes_provider = incidentes_provider
        self.resizable(False, False)

        controles = tk.Frame(self)
        controles.pack(fill="x", pady=8)

        ttk.Label(controles, text="Ordenar por:").pack(side="left", padx=5)
        self.criterio = ttk.Combobox(
            controles, values=self.OPCIONES, state="readonly", width=28
        )
        self.criterio.current(0)
        self.criterio.pack(side="left", padx=5)
        ttk.Button(controles, text="Ordenar", command=self.ordenarHistorial).pack(
            side="left", padx=5
        )

        self.tabla = ttk.Treeview(self, columns=("c1", "c2", "c3"), show="headings")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.ordenarHistorial()

    def ordenarHistorial(self):
        criterio = self.criterio.get()
        incidentes = self.incidentes_provider()
        self.tabla.delete(*self.tabla.get_children())

        if criterio == "Más antiguos":
            ordenados = srt.sorter.mergeSort(incidentes, key=lambda i: i.timestamp)
            self._configurarColumnas("ID", "Ubicación", "Reportado")
            for inc in ordenados:
                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        inc.id,
                        inc.ubicacion,
                        inc.timestamp.strftime("%Y-%m-%d %H:%M"),
                    ),
                )

        elif criterio == "Más críticos":
            ordenados = srt.sorter.quickSort(incidentes, key=lambda i: -i.prioridad)
            self._configurarColumnas("ID", "Prioridad", "Estado")
            for inc in ordenados:
                self.tabla.insert("", "end", values=(inc.id, inc.prioridad, inc.estado))

        else:
            frecuencia = {}
            for inc in incidentes:
                frecuencia[inc.ubicacion] = frecuencia.get(inc.ubicacion, 0) + 1
            pares = srt.sorter.mergeSort(
                list(frecuencia.items()), key=lambda par: -par[1]
            )
            self._configurarColumnas("Zona", "N° Incidentes", "")
            for zona, cantidad in pares:
                self.tabla.insert("", "end", values=(zona, cantidad, ""))

    def _configurarColumnas(self, c1, c2, c3):
        self.tabla.heading("c1", text=c1)
        self.tabla.heading("c2", text=c2)
        self.tabla.heading("c3", text=c3)


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_view = mainView(self)
        self.bottom_info = BottomInfo(self)
        self.sidebar = Sidebar(self)

        self.main_view.grid(row=0, column=0, sticky="nsew")
        self.bottom_info.grid(row=1, column=0, sticky="ew")
        self.sidebar.grid(row=0, column=1, rowspan=2, sticky="ns")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        plt.close("all")
        self.quit()
        self.destroy()
