from structures import hashTable as ht
from structures import pHeap as pq


class IncidentRepo:
    def __init__(self):
        self.hash_table = ht.hashTable(1, 2)
        self.priority_queue = pq.pHeap(1)

    def load(self, parser, filepath):
        for incident in parser.parseFile(filepath):
            self.hash_table.insertar
            self.priority_queue.insert
