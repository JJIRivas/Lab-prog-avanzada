import json
import random
import sys
import time

sys.path.insert(0, ".")

import centerRepo
import incidentRepo
import urgencyManager
from adts import roadNetwork
from structures import hashTable as ht
from structures import pHeap as pq
from structures import search as s
from structures import sorter as srt

random.seed(7)

resultados = {}


# HASHING
repo_temp = incidentRepo.IncidentRepo()
tabla_progresion = ht.hashTable(1)
incidentes_todos = list(repo_temp.parser.parseFile("dataset/incidentes.csv"))

progresion = []
for i, inc in enumerate(incidentes_todos, start=1):
    tabla_progresion.insertar(inc.id, inc)
    if i % 25 == 0 or i == len(incidentes_todos):
        progresion.append(
            {
                "n": i,
                "size": tabla_progresion.size,
                "factor_carga": round(tabla_progresion.factorCarga(), 4),
                "colisiones": tabla_progresion.colisiones,
                "cubetas_ocupadas": tabla_progresion.cubetasOcupadas(),
                "max_tam_cubeta": tabla_progresion.maxTamCubetas(),
                "rehashes": tabla_progresion.rehashes,
            }
        )

resultados["hashing"] = {
    "progresion": progresion,
    "reporte_final": tabla_progresion.reporte(0),
}

# HEAP
heap_bench = pq.pHeap(1)

inicio = time.perf_counter()
for inc in incidentes_todos:
    heap_bench.insert(inc)
tiempo_insert_total = time.perf_counter() - inicio

inicio = time.perf_counter()
extraidos = []
while True:
    x = heap_bench.extractUrgent()
    if x is None:
        break
    extraidos.append(x)
tiempo_extract_total = time.perf_counter() - inicio

# Verificacion de orden: cada extraido debe tener prioridad (al momento de extraerlo)
# mayor o igual al siguiente -> ya se perdio el valor exacto, pero podemos verificar
# que la severidad*factor de cuando se calculo era no creciente en la practica
# (chequeo mas simple: el heap nunca deberia haber quedado con elementos luego del bucle)
resultados["heap"] = {
    "n": len(incidentes_todos),
    "tiempo_insert_total_seg": round(tiempo_insert_total, 6),
    "tiempo_insert_promedio_seg": round(tiempo_insert_total / len(incidentes_todos), 8),
    "tiempo_extract_total_seg": round(tiempo_extract_total, 6),
    "tiempo_extract_promedio_seg": round(
        tiempo_extract_total / len(incidentes_todos), 8
    ),
    "extraidos_ok": len(extraidos) == len(incidentes_todos),
}

# SORTING
sorting_resultados = []
for n in [50, 100, 250, 500]:
    muestra = random.sample(incidentes_todos, n)
    tiempos = srt.sorter.comparar(muestra, key=lambda i: i.timestamp)
    sorting_resultados.append({"n": n, **{k: round(v, 6) for k, v in tiempos.items()}})

resultados["sorting"] = sorting_resultados

# GRAFOS
red = roadNetwork.roadNetwork(1)
red.cargarNodos("dataset/nodos.csv")
red.cargarAristas("dataset/aristas.csv", bidireccional=True)

centros_repo = centerRepo.EmergencyCenterRepo()
centros_repo.load("dataset/centros.csv")

um = urgencyManager.urgencyManager(repo_temp, red, centros_repo.centros)

centro_fijo = centros_repo.centros[0]
zonas = sorted(set(inc.ubicacion for inc in incidentes_todos))
muestra_zonas = random.sample(zonas, min(30, len(zonas)))

comparacion_busqueda = {"bfs": [], "ucs": [], "astar": []}
for zona in muestra_zonas:
    for algoritmo in ["bfs", "ucs", "astar"]:
        inicio = time.perf_counter()
        resultado = um._buscarRuta(centro_fijo.ubicacion, zona, algoritmo)
        tiempo = time.perf_counter() - inicio
        comparacion_busqueda[algoritmo].append(
            {
                "destino": zona,
                "nodos_visitados": len(resultado["visitados"]),
                "costo_total": resultado["costo_total"],
                "tiempo_seg": tiempo,
            }
        )

resumen_busqueda = {}
for algoritmo, corridas in comparacion_busqueda.items():
    nodos = [c["nodos_visitados"] for c in corridas]
    tiempos = [c["tiempo_seg"] for c in corridas]
    resumen_busqueda[algoritmo] = {
        "nodos_visitados_promedio": round(sum(nodos) / len(nodos), 2),
        "nodos_visitados_min": min(nodos),
        "nodos_visitados_max": max(nodos),
        "tiempo_promedio_seg": round(sum(tiempos) / len(tiempos), 8),
    }

resultados["busqueda"] = {
    "centro_usado": centro_fijo.nombre,
    "n_destinos_probados": len(muestra_zonas),
    "resumen": resumen_busqueda,
    "detalle": comparacion_busqueda,
}

# verificacion end-to-end
repo_full = incidentRepo.IncidentRepo()
repo_full.load("dataset/incidentes.csv")
um_full = urgencyManager.urgencyManager(repo_full, red, centros_repo.centros)

atendidos = 0
sin_ruta = 0
costos = []
while True:
    r = um_full.atenderSiguiente(algoritmo="astar")
    if r is None:
        break
    if r["centro"] is None:
        sin_ruta += 1
    else:
        atendidos += 1
        costos.append(r["costo_total"])

resultados["escenario_integrado"] = {
    "total_procesados": atendidos + sin_ruta,
    "atendidos_con_ruta": atendidos,
    "sin_ruta_encontrada": sin_ruta,
    "costo_promedio_min": round(sum(costos) / len(costos), 2) if costos else None,
    "costo_min": round(min(costos), 2) if costos else None,
    "costo_max": round(max(costos), 2) if costos else None,
}

with open("resultados_benchmark.json", "w") as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

print(json.dumps(resultados["hashing"]["reporte_final"], indent=2, ensure_ascii=False))
print("---")
print(json.dumps(resultados["heap"], indent=2, ensure_ascii=False))
print("---")
print(json.dumps(resultados["sorting"], indent=2, ensure_ascii=False))
print("---")
print(json.dumps(resumen_busqueda, indent=2, ensure_ascii=False))
print("---")
print(json.dumps(resultados["escenario_integrado"], indent=2, ensure_ascii=False))
