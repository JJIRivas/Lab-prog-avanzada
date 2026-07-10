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
<img width="1920" height="1080" alt="proyecto2" src="https://github.com/user-attachments/assets/db27dd26-bcd7-4c95-ace0-b7e5d9bbeb43" />

### Seleccion de un archivo
<img width="1918" height="1066" alt="proyecto3" src="https://github.com/user-attachments/assets/d1c6a863-6420-4ab1-9494-60ef49a7b20a" />

### Vista con todos los archivos cargados
<img width="1909" height="1058" alt="proyecto1" src="https://github.com/user-attachments/assets/f488dd17-9586-486c-9519-cafcd7f52b98" />

### Video de muestra de la ejecucion

https://github.com/user-attachments/assets/0d398207-b8a9-4aaa-aa5c-22c538ea3b96


