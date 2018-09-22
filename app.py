# -*- coding: utf-8 -*-
__author__ = 'David Castillo'
from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
api = Api(app)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


def create_app(config_filename):
    app.register_error_handler(404, page_not_found)
    return app


class Buscaxcne(Resource):
    def get(self, cedula):
        ciudadano = []

        URL = ("http://www.cne.gov.ve/web/registro_electoral/ce.php?" +
        "nacionalidad=V" + "&cedula=" + cedula)
        # Realizamos la petición a la web
        req = requests.get(URL)
        # Comprobamos que la petición nos devuelve un Status Code = 200
        status_code = req.status_code
        if status_code == 200:
            print "ENTRAMOS A LA WEB"
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

        else:
            ciudadano = {'Error': 2,
                    'Descripcion': 'PROBLEMAS DE CONEXION!'}

        return  jsonify(ciudadano)

api.add_resource(Buscaxcne, '/api/venezolano/<cedula>')


@app.route('/', methods=['GET'])
def home():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(debug=True)