import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


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

        t = np.arange(0, 2 * np.pi, 0.01)
        self.ax.plot(t, np.sin(t))
        self.canvas.draw()


class BottomInfo(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="lightgreen", width=400, height=100, **kwargs)
        self.grid_propagate(False)

        self.visitas = tk.IntVar(value=0)
        self.distancia = tk.DoubleVar(value=0.0)
        self.costo = tk.DoubleVar(value=0.0)

        stat1 = tk.Frame(self)
        stat2 = tk.Frame(self)
        stat3 = tk.Frame(self)

        stat1.grid(row=0, column=0, padx=20, pady=10)
        stat2.grid(row=0, column=1, padx=20, pady=10)
        stat3.grid(row=0, column=2, padx=20, pady=10)

        ttk.Label(stat1, text="N° Caminos considerados:").pack(side="left")
        ttk.Label(stat1, textvariable=self.visitas).pack(side="left")

        ttk.Label(stat2, text="Distancia total:").pack(side="left")
        ttk.Label(stat2, textvariable=self.distancia).pack(side="left")

        ttk.Label(stat3, text="Costo acumulado:").pack(side="left")
        ttk.Label(stat3, textvariable=self.costo).pack(side="left")


class Sidebar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="lightcoral", width=250, height=360, **kwargs)
        self.grid_propagate(False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2), weight=1)
        self.rowconfigure(3, weight=10)

        self.fileBtn = ttk.Button(self, text="Import File")
        self.fileBtn.grid(row=0, column=0, pady=1)

        self.addIncidentBtn = ttk.Button(self, text="Add Incident")
        self.addIncidentBtn.grid(row=1, column=0, pady=1)

        self.seeHistoryBtn = ttk.Button(self, text="Incident History")
        self.seeHistoryBtn.grid(row=2, column=0, pady=1)


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
