# HashTable
class hashTable:
    # Los valores de 8 y 0.7 se colocaron al ser parecidos a las implementaciones comunes.
    # Ya que la idea de la tabla es guardar los incidentes, y estos deben ser por lo menos 500, la tabla tendra que necesariamente hacer
    # rehash y crecer.
    def __init__(self, id, size=8, factor_carga_max=0.7):
        self.id = id
        self.size = size
        self.cubetas = [[] for _ in range(size)]
        self.colisiones = 0
        self.elementos_total = 0
        self.factor_carga_max = factor_carga_max
        self.rehashes = 0

    # Formula basada en el taller de hash que se hizo.
    def baseHasher(self, key):
        index = 0
        for i in str(key).encode():
            index = (index * 31 + i) % self.size
        return index

    def insertar(self, key, value):
        self._insertarCrudo(key, value)
        # Hace rehash si es necesario.
        if self.factorCarga() > self.factor_carga_max:
            self._rehash()

    def _insertarCrudo(self, key, value):
        llave = self.baseHasher(key)

        # Se actualiza un valor si tiene la misma llave.
        for i, (k, v) in enumerate(self.cubetas[llave]):
            if k == key:
                self.cubetas[llave][i] = (key, value)
                return

        # Si la anterior operacion no se hizo, pero hay un elemento en la posicion- es una colision.
        if len(self.cubetas[llave]) > 0:
            self.colisiones += 1

        # Finalmente, simplemente se agrega en la posicion los valores.
        self.cubetas[llave].append((key, value))
        self.elementos_total += 1

    # Funcion para hacer rehash. Cambia los valores del objeto que es nuestra tabla y reincerta.
    def _rehash(self):
        viejas_cubetas = self.cubetas
        self.size = self._siguientePrimo(
            self.size * 2
        )  # Se hace que el nuevo tamaño sea primo- al parecer hace que sea mejor distribuido.
        self.cubetas = [[] for _ in range(self.size)]
        self.colisiones = 0
        self.elementos_total = 0
        self.rehashes += 1

        for cubeta in viejas_cubetas:
            for key, value in cubeta:
                self._insertarCrudo(key, value)

    @staticmethod
    def _esPrimo(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def _siguientePrimo(self, n):
        candidato = n if n % 2 != 0 else n + 1
        while not self._esPrimo(candidato):
            candidato += 2
        return candidato

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
        return sum(1 for cubeta in self.cubetas if len(cubeta) > 0)

    def maxTamCubetas(self):
        return max((len(cubeta) for cubeta in self.cubetas), default=0)

    def todos(self):
        return [valor for cubeta in self.cubetas for _clave, valor in cubeta]

    def reporte(self, tiempo):
        return {
            "tiempo": tiempo,
            "elementos": self.elementos_total,
            "size_actual": self.size,
            "factor_carga": self.factorCarga(),
            "colisiones": self.colisiones,
            "cubetas_ocupadas": self.cubetasOcupadas(),
            "max_tam_cubeta": self.maxTamCubetas(),
            "rehashes": self.rehashes,
        }
