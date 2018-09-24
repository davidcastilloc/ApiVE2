# -*- coding: utf-8 -*-
__author__ = 'David Castillo'
import unittest
from cne import buscar


class TestFunciones(unittest.TestCase):

    def test_buscar_devuelve_diccionario_con_los_datos_del_ciudadano(self):
        ciudadano = {}
        ciudadano = buscar(24980047)
        self.assertEqual('DAVID', ciudadano['Nombre1'])

if __name__ == '__main__':
    unittest.main()