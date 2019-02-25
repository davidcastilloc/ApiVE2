# -*- coding: utf-8 -*-
__author__ = 'David Castillo'
from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sslify import SSLify
from cne import buscar
from config import DevelopmentConfig

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = '84a54fa37b591b64e13e2db2ce2bcd7c9c0c310c92d83e61'
app.config.from_object(DevelopmentConfig)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['menu'] = {'rutas': ['home', 'ayuda', 'buscador', 'contribuir'],
                      'iconos': ['fa fa-home', 'fa fa-question',
                                 'fa fa-search', 'fa fa-handshake-o']}

app.config['CORS_HEADERS'] = 'application/json'
sslify = SSLify(app)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')


class Buscaxcne(Resource):
    def get(self, cedula):
        ciudadano = buscar(cedula)
        result = {
            'ciudadano': ciudadano,
        }

        return jsonify(result)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.pug'), 404


def create_app(config_filename):
    app.register_error_handler(404, page_not_found)
    return app


@app.route('/buscador', methods=['GET'])
def buscador():
    return render_template('buscar_ciudadano.html')


@app.route('/contribuir', methods=['GET'])
def contribuir():
    return render_template('contribuir.pug')


@app.route('/ayuda', methods=['GET'])
def ayuda():
    return render_template('ayuda.pug')


@app.route('/home')
@app.route('/')
def home():
    return render_template('/base/layout.pug')


api.add_resource(Buscaxcne, '/api/v1/<cedula>')


if __name__ == '__main__':
    app.run(debug='false')
