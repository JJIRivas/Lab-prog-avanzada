import centerRepo
import incidentRepo
import urgencyManager
from adts import roadNetwork
from fileHandlers import fileBrowser
from ui import AddIncidentDialog, HistoryWindow, MainApplication


# Instancia UI y maneja algunas funciones relacionadaos a esta. Ademas de iniciar Repos necesarios.
class main:
    def __init__(self):
        self.app = MainApplication()

        self.incident_repo = incidentRepo.IncidentRepo()
        self.center_repo = centerRepo.EmergencyCenterRepo()
        self.road_network = roadNetwork.roadNetwork(1)
        self.urgency_manager = urgencyManager.urgencyManager(
            self.incident_repo, self.road_network, self.center_repo.centros
        )
        self.auto_activo = False

        self.app.sidebar.btnImportIncicentes.config(command=self.importIncidentes)
        self.app.sidebar.btnImportLugares.config(command=self.importLugares)
        self.app.sidebar.btnImportCaminos.config(command=self.importCaminos)
        self.app.sidebar.btnImportarCentros.config(command=self.importarCentros)
        self.app.sidebar.btnAtender.config(command=self.atenderSiguiente)
        self.app.sidebar.btnAuto.config(command=self.toggleAuto)
        self.app.sidebar.btnIncidentNuev.config(command=self.anadirIncidente)
        self.app.sidebar.btnHistorial.config(command=self.mostrarHistorial)

        self.app.mainloop()

    def anadirIncidente(self):
        AddIncidentDialog(self.app, self.incident_repo.agregarManual)

    def mostrarHistorial(self):
        HistoryWindow(self.app, self.incident_repo.obtenerTodos)

    def importIncidentes(self):
        fp = fileBrowser.browseFile()
        if fp:
            self.incident_repo.load(fp)

    def importLugares(self):
        fp = fileBrowser.browseFile()
        if fp:
            self.road_network.cargarNodos(fp)
            self._refrescarGrafo()

    def importCaminos(self):
        fp = fileBrowser.browseFile()
        if fp:
            self.road_network.cargarAristas(fp, bidireccional=True)
            self._refrescarGrafo()

    def importarCentros(self):
        fp = fileBrowser.browseFile()
        if fp:
            self.center_repo.load(fp)

    def atenderSiguiente(self):
        resultado = self.urgency_manager.atenderSiguiente()
        self._procesarResultado(resultado)

    def toggleAuto(self):
        self.auto_activo = not self.auto_activo

        if self.auto_activo:
            self.app.sidebar.btnAuto.config(text="Detener Modo Automático")
            self.app.sidebar.btnAtender.config(state="disabled")
            self._cicloAutomatico()
        else:
            self.app.sidebar.btnAuto.config(text="Iniciar Modo Automático")
            self.app.sidebar.btnAtender.config(state="normal")

    def _cicloAutomatico(self):
        if not self.auto_activo:
            return

        resultado = self.urgency_manager.atenderSiguiente()
        sigue_habiendo = self._procesarResultado(resultado)

        if sigue_habiendo:
            self.app.after(200, self._cicloAutomatico)
        else:
            self.auto_activo = False
            self.app.sidebar.btnAuto.config(text="Iniciar Modo Automático")
            self.app.sidebar.btnAtender.config(state="normal")

    def _procesarResultado(self, resultado) -> bool:
        if resultado is None:
            self.app.bottom_info.limpiar("Sin incidentes pendientes")
            self._refrescarGrafo()
            return False

        if resultado["centro"] is None:
            self.app.bottom_info.limpiar(f"{resultado['incidente'].id}: sin ruta")
            self._refrescarGrafo()
            return True

        self.app.bottom_info.actualizar(
            incidente_id=resultado["incidente"].id,
            centro_nombre=resultado["centro"].nombre,
            num_visitados=len(resultado["nodos_visitados"]),
            costo_total=resultado["costo_total"],
        )
        self._refrescarGrafo(ruta=resultado["ruta"])
        return True

    def _refrescarGrafo(self, ruta=None):
        self.app.main_view.dibujarGrafo(self.road_network.grafo, ruta=ruta)


if __name__ == "__main__":
    main()
