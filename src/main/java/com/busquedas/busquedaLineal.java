package com.busquedas;

import java.util.Random;
import java.util.Scanner;

class Lineal {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Random numGen = new Random();

        System.out.print("Introduce el numero de filas (n): ");

        int fil = sc.nextInt();

        System.out.print("Introduce el numero de columnas (m): ");

        int col = sc.nextInt();

        int[][] matriz = new int[fil][col];

        System.out.println(
            "\n" + "Matriz de " + fil + " x " + col + " generada:" + "\n"
        );
        for (int i = 0; i < fil; i++) {
            for (int j = 0; j < col; j++) {
                matriz[i][j] = numGen.nextInt(1000001);
                System.out.print("\t" + matriz[i][j] + " ");
            }
            System.out.println();
        }

        System.out.print("\n" + "¿Que numero quieres buscar? ");
        int buscar = sc.nextInt();
        boolean encontrado = false;

        for (int i = 0; i < fil; i++) {
            for (int j = 0; j < col; j++) {
                if (matriz[i][j] == buscar) {
                    System.out.println(
                        "\n" +
                            "Encontrado en fila: " +
                            (i + 1) +
                            " columna: " +
                            (j + 1)
                    );
                    encontrado = true;
                }
            }
        }

        if (!encontrado) System.out.println("El numero no está en la matriz");
        sc.close();
    }
}
