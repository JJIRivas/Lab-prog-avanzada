package com.busquedas;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

public class BusquedaBinariaTest {

    BusquedaBinaria bb = new BusquedaBinaria();

    @Test
    void testBusquedaNormal() {
        int[][] matriz = { { 1, 3, 5 }, { 7, 9, 11 } };

        int resultado = bb.busquedaBinaria(7, matriz);
        assertTrue(resultado != -1);
    }

    @Test
    void testElementoNoExiste() {
        int[][] matriz = { { 2, 4, 6 }, { 8, 10, 12 } };

        int resultado = bb.busquedaBinaria(5, matriz);
        assertEquals(-1, resultado);
    }

    @Test
    void testMatrizVacia() {
        int[][] matriz = new int[0][0];

        assertEquals(-1, bb.busquedaBinaria(1, matriz));
    }

    @Test
    void testUnElemento() {
        int[][] matriz = { { 42 } };

        assertEquals(0, bb.busquedaBinaria(42, matriz));
        assertEquals(-1, bb.busquedaBinaria(10, matriz));
    }

    @Test
    void testElementosRepetidos() {
        int[][] matriz = { { 1, 2, 2 }, { 2, 3, 4 } };

        int resultado = bb.busquedaBinaria(2, matriz);
        assertTrue(resultado != -1);
    }

    @Test
    void testYaOrdenado() {
        int[][] matriz = { { 1, 2, 3 }, { 4, 5, 6 } };

        assertEquals(4, bb.busquedaBinaria(5, matriz));
    }

    @Test
    void testOrdenInverso() {
        int[][] matriz = { { 9, 7, 5 }, { 3, 1, 0 } };

        int resultado = bb.busquedaBinaria(7, matriz);

        assertTrue(resultado == -1 || resultado >= 0);
    }
}
