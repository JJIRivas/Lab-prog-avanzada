import java.util.Arrays;
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

        sc.close();
    }
}
