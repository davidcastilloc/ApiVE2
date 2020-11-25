# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from fastapi import status
from modules.models import Ciudadano
from modules.helpers import Parse, ParseNombre
from modules.ConectionManager import ConsultarDatos


registro_electoral_xpath = '//td/b/font/text()|//td/b/text()|//td/text()|//td/font/text()'
registro_civil_xpath = '//td//b/text()'


CI_NO_REGISTRADA = 404
CI_FALLECIDO = 401


class CiudadanoException(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code


class Buscar:
    def get_ciudadano(self, nacionalidad, cedula):
        ciudadano = self._get_registro_nacional_electoral(nacionalidad, cedula)
        if ciudadano is CI_NO_REGISTRADA:
            ciudadano = self._get_registro_civil(nacionalidad, cedula)
            if ciudadano is CI_NO_REGISTRADA:
                return status.HTTP_404_NOT_FOUND
            return ciudadano
        return ciudadano


    def _get_registro_civil(nacionalidad, cedula):
        html = ConsultarDatos(nacionalidad, cedula).registro_civil()
        data = Selector(text=html).xpath(registro_civil_xpath).extract()
        if not data:
            raise CiudadanoException(
                message=f"Error! la cedula {nacionalidad}-{cedula} no esta registrada en la base de datos.",
                code=CI_NO_REGISTRADA
            )
        pn = ParseNombre(html)
        return Ciudadano(
            id=int(cedula),
            nacionalidad="Venezolano" if nacionalidad == "V" else "Extranjero",
            cedula=nacionalidad + "-" + str(cedula),
            nombre_completo=pn.nombre_completo,
            nombres=pn.nombre_de_pila,
            apellidos=pn.apellidos,
            estado="N/A",
            municipio="N/A",
            parroquia="N/A",
            centro="N/A",
            direccion="N/A"
        )


    def _get_registro_nacional_electoral(nacionalidad: str, cedula: int):
        html = ConsultarDatos(nacionalidad, cedula).registro_nacional_electoral()
        data = Selector(text=html).xpath(registro_electoral_xpath).extract()
        if data[3].find("Registro") == 0:
            return CI_NO_REGISTRADA
        elif data[3] == " FALLECIDO (3)":
            raise CiudadanoException(
                message=f"Error! la cedula {nacionalidad}-{cedula} pertenece a un ciudadano fallecido...",
                code=CI_FALLECIDO
            )
        pn = ParseNombre(html)
        p = Parse()
        return Ciudadano(
            id=int(cedula),
            nacionalidad="Venezolano" if nacionalidad == "V" else "Extranjero",
            cedula=int(cedula),
            nombre_completo=pn.nombre_completo,
            nombres=pn.nombre_de_pila,
            apellidos=pn.apellidos,
            estado=p.parse_edo(data[data.index('Estado:') + 1]).title(),
            municipio=p.parse_mp(data[data.index('Municipio:') + 1]).title(),
            parroquia=p.parse_pq(data[data.index('Parroquia:') + 1]).title(),
            centro=p.parse_txt(data[data.index('Centro:') + 1]).title(),
            direccion=p.parse_txt(data[data.index('Dirección:') + 1]).capitalize()
        )
