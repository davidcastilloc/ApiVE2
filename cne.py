# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


def buscar(cedula):
        #Creamos una variable para almacenar dentro de ella los
        #datos del ciudadano

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

            #Si no se encontro la cedula
            if len(datos) < 1:
                #preguntamos el motivo para rellenar la descripcion del error
                datos = html.find_all('td')
                motivo = 0
                # Si el scrapper me devuelve 3 significa que la cedula pertenece
                #a un fallecido :(
                if (datos[19].getText()[-2] == "3"):
                    motivo = 3
                    descripcion = "El número de cédula ingresado pertenece a un ciudadano fallecido."
                else:
                    motivo = 2
                    descripcion = "El ciudadano no esta registrado en nuestra base de datos."
                ciudadano = {
                    'error': True,
                    'tipo': motivo,
                    'descripcion': descripcion
                }
            else:
                ciudadano = {
                    'error': False,
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
                #nombre_completo = ["DAVID" ,"JOSE","CASTILLO", "CIRILO"]
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
                    ciudadano['primerApellido'] = nombre_completo[-1]
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
            ciudadano = {'error': True,
                         'tipo': '{c}'.format(c=type(e).__name__),
                         'descripcion': str(e)}

        return ciudadano
