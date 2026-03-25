package com.busquedas;

import java.util.Random;

public class BusquedaLineal {

    public int[][] generarMatriz(int fil, int col) {
        Random rand = new Random();
        int[][] matriz = new int[fil][col];

        for (int i = 0; i < fil; i++) {
            for (int j = 0; j < col; j++) {
                matriz[i][j] = rand.nextInt(1000001);
            }
        }

        return matriz;
    }

    public int busquedaLineal(int objetivo, int[][] matriz) {
        if (matriz == null || matriz.length == 0 || matriz[0].length == 0) {
            return -1;
        }

        int columnas = matriz[0].length;

        for (int i = 0; i < matriz.length; i++) {
            for (int j = 0; j < columnas; j++) {
                if (matriz[i][j] == objetivo) {
                    return i * columnas + j;
                }
            }
        }

        return -1;
    }
}
