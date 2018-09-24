# -*- coding: utf-8 -*-
__author__ = 'David Castillo'
from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api
from cne import buscar

app = Flask(__name__)
api = Api(app)


class Buscaxcne(Resource):
    def get(self, cedula):
        ciudadano = buscar(cedula)
        return  jsonify(ciudadano)

api.add_resource(Buscaxcne, '/api/venezolano/<cedula>')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


def create_app(config_filename):
    app.register_error_handler(404, page_not_found)
    return app


@app.route('/buscador', methods=['GET'])
def buscador():
    return render_template('buscar_ciudadano.html')


@app.route('/contribuir', methods=['GET'])
def contribuir():
    return render_template('contribuir.html')


@app.route('/ayuda', methods=['GET'])
def ayuda():
    return render_template('ayuda.html')


@app.route('/', methods=['GET'])
def home():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(debug=True)