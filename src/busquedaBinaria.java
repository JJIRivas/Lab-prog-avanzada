import java.util.Arrays;
import java.util.LinkedList;
import java.util.Random;
import java.util.Scanner;

class Binario {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Introduce el numero de filas (n): ");

        int fil = sc.nextInt();

        System.out.print("Introduce el numero de columnas (m): ");

        int col = sc.nextInt();

        System.out.println("\n" + "Matriz creada: " + "\n");

        int[][] matriz = arrSetup(fil, col);

        System.out.print("\n" + "Numero a buscar: ");
        int resultado = busquedaBin(sc.nextInt(), matriz);
        if (resultado == -1) {
            System.out.println("Numero no esta en la matriz.");
            sc.close();
            System.exit(resultado);
        }
        System.out.println("Numero encontrado en la posicion: " + resultado);

        sc.close();
    }

    public static int busquedaBin(int n, int[][] matFinal) {
        int filas = matFinal.length;
        int colum = matFinal[0].length;
        int min = 0;
        int max = filas * colum - 1;

        while (min <= max) {
            int med = min + (max - min) / 2;
            /*System.out.println(
                "min: " + min + "\n med: " + med + "\n max: " + max
                );*/
            int medValue = matFinal[med / colum][med % colum];
            // System.out.println("x: " + (med / colum) + " y: " + (med % colum));

            if (medValue == n) return med + 1;
            if (medValue < n) min = med + 1;
            else max = med - 1;
        }

        return -1;
    }

    public static int[][] arrSetup(int fil, int col) {
        Random numGen = new Random();
        int[][] mat = new int[fil][col];

        for (int i = 0; i < fil; i++) {
            for (int j = 0; j < col; j++) {
                mat[i][j] = numGen.nextInt(1001);
            }
        }

        int[] arr = new int[fil * col];

        int index = 0;
        for (int i = 0; i < fil; i++) {
            for (int j = 0; j < col; j++) {
                arr[index++] = mat[i][j];
            }
        }

        index = 0;
        Arrays.sort(arr);

        for (int i = 0; i < fil; i++) {
            for (int j = 0; j < col; j++) {
                mat[i][j] = arr[index++];
                System.out.print("\t" + mat[i][j] + " ");
            }
            System.out.println();
        }

        return mat;
    }
}
