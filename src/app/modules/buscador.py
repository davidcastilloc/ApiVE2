# -*- coding: utf-8 -*-
from fastapi import status
from scrapy.selector import Selector

from modules.ConectionManager import ConsultarDatos
from modules.helpers import Parse, ParseNombre
from modules.models import Ciudadano


class CiudadanoException(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code


class Buscar:
    CI_NO_REGISTRADA = 404
    CI_FALLECIDO = 400
    nacionalidad = 0
    cedula = ""
    registro_electoral_xpath = '//td/b/font/text()|//td/b/text()|//td/text()|//td/font/text()'
    registro_civil_xpath = '//td//b/text()'
    
    def __init__(self, nacionalidad: str, cedula: int):
        self.nacionalidad = nacionalidad.upper()
        self.cedula = cedula
        
    def get_ciudadano(self):
        ciudadano = self._get_registro_nacional_electoral()
        if ciudadano is self.CI_NO_REGISTRADA:
            ciudadano = self._get_registro_civil()
        return ciudadano

    def _get_registro_civil(self):
        html = ConsultarDatos(self.nacionalidad, self.cedula).registro_civil()
        data = Selector(text=html).xpath(self.registro_civil_xpath).extract()
        print(data)
        if not data:
            raise CiudadanoException(
                message=f"Error! la cedula {self.nacionalidad}-{self.cedula} no esta registrada en la base de datos.",
                code=self.CI_NO_REGISTRADA
            )
        pn = ParseNombre(html)
        return Ciudadano(
            id=int(self.cedula),
            nacionalidad="Venezolano" if self.nacionalidad == "V" else "Extranjero",
            cedula=int(self.cedula),
            nombre_completo=pn.nombre_completo,
            nombres=pn.nombre_de_pila,
            apellidos=pn.apellidos,
            estado="N/A",
            municipio="N/A",
            parroquia="N/A",
            centro="N/A",
            direccion="N/A"
        )

    def _get_registro_nacional_electoral(self):
        try:
            html = ConsultarDatos(
                self.nacionalidad, self.cedula).registro_nacional_electoral()
            data = Selector(text=html).xpath(self.registro_electoral_xpath).extract()
            if data[2].find("Registro") == 0:
                return self.CI_NO_REGISTRADA
            if data[4] == " FALLECIDO (3)":
                raise CiudadanoException(
                    message=f"Error! la cedula {self.nacionalidad}-{self.cedula} pertenece a un ciudadano fallecido...",
                    code=self.CI_FALLECIDO
                )
            pn = ParseNombre(html)
            p = Parse()
        except IndexError:
            print("Error! la cedula no esta registrada en la base de datos.")
            return self.CI_NO_REGISTRADA
        return Ciudadano(
            id=int(self.cedula),
            nacionalidad="Venezolano" if self.nacionalidad == "V" else "Extranjero",
            cedula=int(self.cedula),
            nombre_completo=pn.nombre_completo,
            nombres=pn.nombre_de_pila,
            apellidos=pn.apellidos,
            estado=p.parse_edo(data[data.index('Estado:') + 1]).title(),
            municipio=p.parse_mp(data[data.index('Municipio:') + 1]).title(),
            parroquia=p.parse_pq(data[data.index('Parroquia:') + 1]).title(),
            centro=p.parse_txt(data[data.index('Centro:') + 1]).title(),
            direccion=p.parse_txt(
                data[data.index('Dirección:') + 1]).capitalize()
        )
