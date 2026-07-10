from fileHandlers import edgeParser as ep
from fileHandlers import nodeParser as np_
from structures import graph as g


# Representa los caminos y lugares. Ocupa los parsers necesarios para instanciarse y tiene funciones para agregar cada uno.
class roadNetwork:
    def __init__(self, id):
        self.id = id
        self.grafo = g.graph()
        self.node_parser = np_.nodeParser()
        self.edge_parser = ep.edgeParser()

    def cargarNodos(self, filepath):
        for nombre, lat, lon in self.node_parser.parseFile(filepath):
            self.grafo.agregarNodo(nombre, lat=lat, lon=lon)

    def cargarAristas(self, filepath, bidireccional=False):
        for origen, destino, peso in self.edge_parser.parseFile(filepath):
            self.grafo.agregarArista(origen, destino, peso, bidireccional)
