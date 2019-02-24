# -*- coding: utf-8 -*-
__author__ = 'David Castillo'
import unittest
from cne import buscar

	
def displatDict(dictOfElements) :
    for key , value in dictOfElements.items():
        print(key, " :: ", value)

class TestFunciones(unittest.TestCase):

    def test_buscar_devuelve_diccionario_con_los_datos_del_ciudadano(self):
        ciudadano = {}
        ciudadano = buscar(24980047)
        print("Funcion de busqueda ejecutada!")
        self.assertEqual('DAVID', ciudadano['primerNombre'])

    def test_buscar_delvuelve_los_resultados_correctamente(self):
    	ciudadano = {}
    	ciudadano = buscar(7654321)
    	displatDict(ciudadano)

if __name__ == '__main__':
    unittest.main()
