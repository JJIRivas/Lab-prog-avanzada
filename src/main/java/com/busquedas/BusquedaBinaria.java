package com.busquedas;

import java.util.Arrays;
import java.util.Random;

public class BusquedaBinaria {

    public int[][] generarMatriz(int fil, int col) {
        Random rand = new Random();
        int[] arr = new int[fil * col];

        for (int i = 0; i < arr.length; i++) {
            arr[i] = rand.nextInt(1000001);
        }

        Arrays.sort(arr);

        int[][] mat = new int[fil][col];
        int index = 0;

        for (int i = 0; i < fil; i++) {
            for (int j = 0; j < col; j++) {
                mat[i][j] = arr[index++];
            }
        }

        return mat;
    }

    public int busquedaBinaria(int n, int[][] matriz) {
        if (matriz == null || matriz.length == 0 || matriz[0].length == 0) {
            return -1;
        }

        int filas = matriz.length;
        int columnas = matriz[0].length;

        int min = 0;
        int max = filas * columnas - 1;

        while (min <= max) {
            int medio = min + (max - min) / 2;
            int valorMedio = matriz[medio / columnas][medio % columnas];

            if (valorMedio == n) return medio;
            if (valorMedio < n) min = medio + 1;
            else max = medio - 1;
        }

        return -1;
    }
}
