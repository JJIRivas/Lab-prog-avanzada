# Proyecto Integrador Final - Sistema Inteligente de Gestión y Optimización de Rutas de Emergencia.
El codigo actual es un programa que tiene como objetivo el, dado la correcta informacion, priorizar incidentes en cases de emergencia y mostrar la mejor ruta de un centro de emergencia hasta estos.

El informe comenta mas a fondo sobre algunas cosas.

## Ejecucion
Luego de clonar el repositorio, basta con correr main para iniciar el programa, esto se hace mediante:
```
$ python3 main.py
```
En la carpeta del programa.

Una vez iniciado, es seguir el orden que tienen los botones, cargando primero los archivos relevantes que tengan la informacion (los cuales estan proporcionados en la carpeta de dataset/), y luego oprimiendo "Atender Siguiente" o "Iniciar Modo Automatico".

Siendo especifico, el orden que se debe seguir es:

1) Cargar Puntos de la Red
2) Cargar Calles
3) Cargar Centros de Emergencia
4) Cargar Incidentes
5) Correr

Para correr el benchmark, basta con estar en la carpeta del proyecto y correr:
```
$ python3 benchmark.py
```

## Media

### Inicio programa
### Seleccion de un archivo
### Vista con todos los archivos cargados
### Video de muestra de la ejecucion
![alt-text][media/videoDemostracion.mp4]
