# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


def buscar(cedula):
        ciudadano = []

        URL = ("http://www.cne.gov.ve/web/registro_electoral/ce.php?" +
               "nacionalidad=V" + "&cedula=" + str(cedula))

        # Realizamos la petición a la web
        try:
            req = requests.get(URL)
            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(req.text, "html.parser")

            # Obtenemos todos los td donde están los datos del ciudadano
            datos = html.find_all('td', {'align': 'left'})

            if len(datos) < 1:
                ciudadano = {
                    'Error': True,
                    'descripcion': 'CIUDADANO NO ENCONTRADO!'
                }
            else:
                ciudadano = {
                    'nacionalidad': 'V',
                    'cedula': int(cedula),
                    'estado': datos[5].getText(),
                    'municipio': datos[7].getText(),
                    'parroquia': datos[9].getText(),
                    'centro': datos[11].getText(),
                    'direccion': datos[13].getText()
                }

                # si el ciudadano tiene un solo nombre devuelve True
                un_nombre = str(datos[3]).find(' </b>') > 0
                # si el ciudadano tiene un solo apellido devuelve True
                un_apellido = str(datos[3]).find('  ') > 0
                nombre_completo = datos[3].getText().split()
                # SI EL NOMBRE_COMPLETO CONTIENE 4 FRASES O MAS
                if len(nombre_completo) <= 4:
                    if (un_apellido):
                        ciudadano['primerNombre'] = nombre_completo[0]
                        ciudadano['segundoNombre'] = nombre_completo[1]
                        # obtenemos el apellido apuntando al ultimo item -1
                        ciudadano['primerApellido'] = nombre_completo[-1]
                    else:
                        # COLOCAMOS LOS NOMBRES Y APELLIDOS DONDE VAN
                        ciudadano['primerNombre'] = nombre_completo[0]
                        ciudadano['segundoNombre'] = nombre_completo[1]
                        ciudadano['primerApellido'] = nombre_completo[2]
                        ciudadano['segundoApellido'] = nombre_completo[3]
                elif(len(nombre_completo) == 2):
                    ciudadano['primerNombre'] = nombre_completo[0]
                    ciudadano['Apellido1'] = nombre_completo[-1]
                elif(len(nombre_completo) == 3):
                    if (un_nombre):
                        ciudadano['primerNombre'] = nombre_completo[0]
                        ciudadano['segundoNombre'] = nombre_completo[1]
                        ciudadano['primerApellido'] = nombre_completo[2]
                    else:
                        ciudadano['primerNombre'] = nombre_completo[0]
                        ciudadano['primerApellido'] = nombre_completo[1]
                        ciudadano['segundoApellido'] = nombre_completo[2]
                elif nombre_completo[1] is "DEL" or "DEL ":
                    ciudadano['primerNombre'] = nombre_completo[0]
                    ciudadano['segundoNombre'] = nombre_completo[1]+ " " + nombre_completo[2]
                    ciudadano['primerApellido'] = nombre_completo[3]
                    ciudadano['segundoApellido'] = nombre_completo[4]
                ciudadano['nombreCompleto'] = datos[3].getText()
            
        except Exception as e:
            ciudadano = {'Error': True,
                         'Tipo': '{c}'.format(c=type(e).__name__),
                         'Descripcion': str(e)}

        return ciudadano
