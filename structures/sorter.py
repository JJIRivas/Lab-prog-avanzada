import random
import time


class sorter:
    @staticmethod
    def mergeSort(datos, key=lambda x: x):
        if len(datos) <= 1:
            return list(datos)

        medio = len(datos) // 2
        izquierda = sorter.mergeSort(datos[:medio], key)
        derecha = sorter.mergeSort(datos[medio:], key)
        return sorter._merge(izquierda, derecha, key)

    @staticmethod
    def _merge(izquierda, derecha, key):
        resultado = []
        i = j = 0
        while i < len(izquierda) and j < len(derecha):
            if key(izquierda[i]) <= key(derecha[j]):
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        # Agrega lo que haya quedado sin comparar.
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado

    @staticmethod
    def quickSort(datos, key=lambda x: x):
        datos = list(datos)
        sorter._quickSortInPlace(datos, 0, len(datos) - 1, key)
        return datos

    @staticmethod
    def _quickSortInPlace(datos, bajo, alto, key):
        if bajo < alto:
            pivote_idx = sorter._particionar(datos, bajo, alto, key)
            sorter._quickSortInPlace(datos, bajo, pivote_idx - 1, key)
            sorter._quickSortInPlace(datos, pivote_idx + 1, alto, key)

    @staticmethod
    def _particionar(datos, bajo, alto, key):
        # pivote aleatorio para evitar O(n^2) con datos ya ordenadoso o semi.
        pivote_random = random.randint(bajo, alto)
        datos[pivote_random], datos[alto] = datos[alto], datos[pivote_random]

        pivote = key(datos[alto])
        i = bajo - 1
        for j in range(bajo, alto):
            if key(datos[j]) <= pivote:
                i += 1
                datos[i], datos[j] = datos[j], datos[i]
        datos[i + 1], datos[alto] = datos[alto], datos[i + 1]
        return i + 1

    @staticmethod
    def comparar(datos, key=lambda x: x, algoritmos=None):
        algoritmos = algoritmos or {
            "mergeSort": sorter.mergeSort,
            "quickSort": sorter.quickSort,
        }
        resultados = {}
        for nombre, funcion in algoritmos.items():
            inicio = time.perf_counter()  # Deberia ser mas preciso que time.time().
            funcion(datos, key)
            fin = time.perf_counter()
            resultados[nombre] = fin - inicio
        return resultados
