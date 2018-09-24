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
            #status_code = req.status_code
            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(req.text, "html.parser")

            # Obtenemos todos los td donde están los datos del ciudadano
            datos = html.find_all('td', {'align': 'left'})
            if len(datos) < 3:
                ciudadano = {'Error': 1,
                    'Descripcion': 'CIUDADANO NO ENCONTRADO!'}
            else:
                ciudadano = {
                        'Nacionalidad': 'VENEZOLANO',
                        'Cédula': int(cedula),
                        'Nombre1': datos[3].getText().split()[0],
                        'Nombre2': datos[3].getText().split()[1],
                        'Apellido1': datos[3].getText().split()[2],
                        'Apellido2': datos[3].getText().split()[3],
                        'Estado': datos[5].getText(),
                        'Municipio': datos[7].getText(),
                        'Parroquia': datos[9].getText(),
                        'Centro': datos[11].getText(),
                        'Dirección': datos[13].getText()
                        }
        except Exception:
            ciudadano = {'Error': 2,
                  'Descripcion': 'El servicio de datos del CNE esta Offline!'}

        return  ciudadano