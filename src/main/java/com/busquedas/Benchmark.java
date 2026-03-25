package com.busquedas;

import java.util.Arrays;
import java.util.Random;

public class Benchmark {

    public static void main(String[] args) {
        BusquedaBinaria bb = new BusquedaBinaria();
        BusquedaLineal bl = new BusquedaLineal();
        Random rand = new Random();

        int[] tamanos = { 100, 500, 1000, 5000, 10000, 20000 };
        int repeticiones = 20;

        for (int n : tamanos) {
            int fil = (int) Math.sqrt(n);
            int col = fil;

            int[][] matrizOrdenada = bb.generarMatriz(fil, col);

            int[][] matrizRandom = bl.generarMatriz(fil, col);

            long[] tiemposBin = new long[repeticiones];
            long[] tiemposLin = new long[repeticiones];

            for (int i = 0; i < repeticiones; i++) {
                int objetivo = matrizOrdenada[rand.nextInt(fil)][rand.nextInt(
                    col
                )];

                long inicio = System.nanoTime();
                bb.busquedaBinaria(objetivo, matrizOrdenada);
                long fin = System.nanoTime();
                tiemposBin[i] = fin - inicio;

                inicio = System.nanoTime();
                bl.busquedaLineal(objetivo, matrizRandom);
                fin = System.nanoTime();
                tiemposLin[i] = fin - inicio;
            }

            Arrays.sort(tiemposBin);
            Arrays.sort(tiemposLin);

            long medianaBin = tiemposBin[repeticiones / 2];
            long medianaLin = tiemposLin[repeticiones / 2];

            System.out.println(
                "Tamaño: " +
                    n +
                    "  Binaria: " +
                    medianaBin +
                    " ns" +
                    "  Lineal: " +
                    medianaLin +
                    " ns"
            );
        }
    }
}
