# -*- coding: utf-8 -*-
__author__ = 'David Castillo'
import unittest
from cne import buscar


class TestFunciones(unittest.TestCase):

    def test_buscar_devuelve_diccionario_con_los_datos_del_ciudadano(self):
        ciudadano = {}
        ciudadano = buscar(24980047)
        print("Funcion de busqueda ejecutada!")
        self.assertEqual('DAVID', ciudadano['primerNombre'])

if __name__ == '__main__':
    unittest.main()
