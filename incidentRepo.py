from datetime import datetime

from adts import incident as inc
from fileHandlers import incidentParser as ip
from structures import hashTable as ht
from structures import pHeap as pq


# Clase para guardar los incidentes, el objeto teniendo la tabla hash y Priority queue asociados, ademas del parser que pasa los incidentes a datos ocupables.
class IncidentRepo:
    def __init__(self):
        self.hash_table = ht.hashTable(1)
        self.priority_queue = pq.pHeap(1)
        self.parser = ip.incidentParser()

    def load(self, filepath):
        for incidente in self.parser.parseFile(filepath):
            self.hash_table.insertar(incidente.id, incidente)
            self.priority_queue.insert(incidente)

    def agregarManual(self, id_, ubicacion, prioridad, tipo, estado="pendiente"):
        nuevo = inc.incident(id_, ubicacion, prioridad, tipo, datetime.now(), estado)
        self.hash_table.insertar(nuevo.id, nuevo)
        self.priority_queue.insert(nuevo)
        return nuevo

    def obtenerTodos(self):
        return self.hash_table.todos()
