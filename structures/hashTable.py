class hashTable:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.cubetas = [[] for _ in range(size)]
        self.colisiones = 0
        self.elementos_total = 0

    def baseHasher(self, key):
        index = 0
        for i in key.encode():
            index = (index * 31 + i) % self.size
        return index

    def insertar(self, key, value):
        llave = self.baseHasher(key)

        for i, (k, v) in enumerate(self.cubetas[llave]):
            if k == key:
                self.cubetas[llave][i] = (key, value)
                return

        if len(self.cubetas[llave]) > 0:
            self.colisiones += 1

        self.cubetas[llave].append((key, value))
        self.elementos_total += 1

    def buscar(self, key):
        llave = self.baseHasher(key)

        for k, v in self.cubetas[llave]:
            if k == key:
                return v
        return None

    def borrar(self, key):
        llave = self.baseHasher(key)
        cubeta = self.cubetas[llave]

        for i, (k, v) in enumerate(cubeta):
            if k == key:
                cubeta.pop(i)
                self.elementos_total -= 1
                return True
        return False

    def factorCarga(self):
        return self.elementos_total / self.size

    def cubetasOcupadas(self):
        ocupadas = 0

        for cubeta in self.cubetas:
            if len(cubeta) > 0:
                ocupadas += 1
        return ocupadas

    def maxTamCubetas(self):
        max = 0
        for cubeta in self.cubetas:
            if len(cubeta) > max:
                max = len(cubeta)
        return max

    def reporte(self, tiempo):
        print("a")
