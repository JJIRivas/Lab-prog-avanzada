package com.busquedas;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

public class BusquedaLinealTest {

    BusquedaLineal bl = new BusquedaLineal();

    @Test
    void testBusquedaNormal() {
        int[][] matriz = { { 5, 3, 8 }, { 1, 9, 2 } };

        assertTrue(bl.busquedaLineal(9, matriz) != -1);
    }

    @Test
    void testNoExiste() {
        int[][] matriz = { { 1, 2 }, { 3, 4 } };

        assertEquals(-1, bl.busquedaLineal(10, matriz));
    }

    @Test
    void testMatrizVacia() {
        int[][] matriz = new int[0][0];
        assertEquals(-1, bl.busquedaLineal(1, matriz));
    }

    @Test
    void testUnElemento() {
        int[][] matriz = { { 7 } };

        assertEquals(0, bl.busquedaLineal(7, matriz));
        assertEquals(-1, bl.busquedaLineal(3, matriz));
    }

    @Test
    void testRepetidos() {
        int[][] matriz = { { 2, 2 }, { 2, 2 } };

        assertTrue(bl.busquedaLineal(2, matriz) != -1);
    }
}
