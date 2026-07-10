from datetime import datetime


# Priority Queue
class pHeap:
    # Implementado como un max heap binario
    def __init__(self, id) -> None:
        self.id = id
        self.heap = []  # cada entrada es prioridad, incidente
        self.pos = {}  # indice en self.heap es incident.id

    # Calcula la prioridad del incidente.
    # No es solo la severidad, ya que esto podria tener el efecto de hacer que los incidentes
    # de baja severidad nunca se resuelvan si llegan mas con mayor severidad antes de que se pueda ver este.
    def calcPriority(self, incident, ahora=None):
        ahora = ahora or datetime.now()  # Si no hay datetime se agrega.
        tiempo_transcurrido_min = (
            ahora - incident.timestamp
        ).total_seconds() / 60  # Tiempo desde el incidente hasta ahora
        factor_tiempo = (
            1 + max(tiempo_transcurrido_min, 0) / 60
        )  # deberia crecer por hora de espera
        severidad = incident.prioridad
        return severidad * factor_tiempo

    def insert(self, incident):
        prioridad = self.calcPriority(incident)
        self.heap.append([prioridad, incident])
        idx = len(self.heap) - 1
        self.pos[incident.id] = idx
        self._siftUp(idx)  # Si corresponde, el nuevo incidente "va hacia arriba"

    # Extrae el mas urgente (0 por ser max heap) y mueve el ultimo + sift down para mantener la estructura.
    def extractUrgent(self):
        if not self.heap:
            return None
        tope = self.heap[0]
        ultimo = self.heap.pop()
        del self.pos[tope[1].id]
        if self.heap:
            self.heap[0] = ultimo
            self.pos[ultimo[1].id] = 0
            self._siftDown(0)
        return tope[1]

    # Recalcula la prioridad de un incidente ya en el heap.
    # Ocupa self.pos para evitar tener que buscar de manera tan ineficiente.
    # Dependiendo de lo que le pase a la prioridad, el heap sube o baja.
    def priorityUpdate(self, incident_id, ahora=None):
        if incident_id not in self.pos:
            return False
        idx = self.pos[incident_id]
        incidente = self.heap[idx][1]
        nueva = self.calcPriority(incidente, ahora)
        vieja = self.heap[idx][0]
        self.heap[idx][0] = nueva
        if nueva > vieja:
            self._siftUp(idx)
        else:
            self._siftDown(idx)
        return True

    def topKCrit(self, k):
        copia = pHeap(self.id)
        copia.heap = [item[:] for item in self.heap]
        copia.pos = dict(self.pos)
        return [copia.extractUrgent() for _ in range(min(k, len(copia.heap)))]

    def _siftUp(self, idx):
        while idx > 0:
            padre = (idx - 1) // 2
            if self.heap[idx][0] > self.heap[padre][0]:
                self._swap(idx, padre)
                idx = padre
            else:
                break

    def _siftDown(self, idx):
        n = len(self.heap)
        while True:
            izq, der, mayor = 2 * idx + 1, 2 * idx + 2, idx
            if izq < n and self.heap[izq][0] > self.heap[mayor][0]:
                mayor = izq
            if der < n and self.heap[der][0] > self.heap[mayor][0]:
                mayor = der
            if mayor == idx:
                break
            self._swap(idx, mayor)
            idx = mayor

    def _swap(self, i, j):
        # Cambia posiciones en el heap entre 2 dados. No es lo mejor pero funciona.
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.pos[self.heap[i][1].id] = i
        self.pos[self.heap[j][1].id] = j
