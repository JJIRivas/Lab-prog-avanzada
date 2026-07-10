# Grafos
class graph:
    def __init__(self):
        self.nodos = set()
        self.adyacencia = {}
        self.metadata = {}

    # Normaliza nombres para trabajarlos mas facil
    @staticmethod
    def normalizar(nombre):
        return str(nombre).strip().lower().replace(" ", "_")

    # Agrega un Nodo/Lugar luego de normalizar. Si no es adyacente ya, entonces se añade para su posicion y se agrega el nodo como tal.
    # Si tiene mas datos asociados, se agrega con una variable opcional a la "metadata". Deberia tener, puesto que seria la ubicacion como tal, pero no es un requerimiento duro.
    def agregarNodo(self, nodo, **datos):
        nodo = self.normalizar(nodo)
        if nodo not in self.adyacencia:
            self.adyacencia[nodo] = []
            self.nodos.add(nodo)
        if datos:
            self.metadata[nodo] = datos

    # Los caminos. Similar a la funcion anterior, pero agrega tuples con peso en base a los nodos de origen y destino con la adyacencia, formando un camino.
    # Se agrega el sentido contrario si la bidireccionalidad es True.
    def agregarArista(self, origen, destino, peso, bidireccional=False):
        origen = self.normalizar(origen)
        destino = self.normalizar(destino)
        self.agregarNodo(origen)
        self.agregarNodo(destino)
        self.adyacencia[origen].append((destino, peso))
        if bidireccional:
            self.adyacencia[destino].append((origen, peso))

    # Retorna las coordenadas de un nodo si es que estan.
    def coordenadas(self, nodo):
        nodo = self.normalizar(nodo)
        datos = self.metadata.get(nodo)
        if datos and "lat" in datos and "lon" in datos:
            return datos["lat"], datos["lon"]
        return None

    # Retorna los nodos con los que tiene caminos. Osea, los vecinos.
    def vecinos(self, nodo):
        nodo = self.normalizar(nodo)
        return self.adyacencia.get(nodo, [])

    def obtenerNodos(self):
        return list(self.nodos)

    def obtenerAristas(self):
        return [
            (origen, destino, peso)
            for origen, lista in self.adyacencia.items()
            for destino, peso in lista
        ]

    def numNodos(self):
        return len(self.nodos)

    def numAristas(self):
        return sum(len(v) for v in self.adyacencia.values())
