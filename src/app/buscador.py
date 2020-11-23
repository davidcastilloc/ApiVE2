# -*- coding: utf-8 -*-
import urllib.request
from scrapy.selector import Selector
from .helpers import Parse, ParseNombre
from .models import Ciudadano
from fastapi import status

registro_electoral_xpath = '//td/b/font/text()|//td/b/text()|//td/text()|//td/font/text()'
registro_civil_xpath = '//td//b/text()'
url_base_cne = 'http://www.cne.gov.ve/web/registro_'
registro_electoral = 'electoral/ce.php?nacionalidad={nac}&cedula={ced}'
registro_civil = 'civil/buscar_rep.php?nacionalidad={nac}&ced={ced}'

CI_NO_REGISTRADA = 404
CI_FALLECIDO = 401


class CiudadanoException(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code


def get_ciudadano(nacionalidad, cedula):
    ciudadano = get_registro_nacional_electoral(nacionalidad, cedula)
    if ciudadano is CI_NO_REGISTRADA:
        ciudadano = get_registro_civil(nacionalidad, cedula)
        if ciudadano is CI_NO_REGISTRADA:
            return status.HTTP_404_NOT_FOUND
        return ciudadano
    return ciudadano


def get_decoded_html(servicio, nacionalidad, cedula):
    url_for_urllib = url_base_cne + servicio.format(nac=nacionalidad, ced=cedula)
    print(url_for_urllib)
    html = urllib.request.urlopen(url_for_urllib)
    decoded = html.read().decode('utf-8')
    return decoded.replace('\t', '').replace('\n', '').replace('\r', '')


def get_registro_civil(nacionalidad, cedula):
    html = get_decoded_html(registro_civil, nacionalidad, cedula)
    data = Selector(text=html).xpath(registro_civil_xpath).extract()
    if not data:
        raise CiudadanoException(
            message=f"Error! la cedula {nacionalidad}-{cedula} no esta registrada en la base de datos.",
            code=CI_NO_REGISTRADA
        )
    pn = ParseNombre(html)
    return Ciudadano(
        nacionalidad="VENEZOLANO" if nacionalidad == "V" else "EXTRANJERO",
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


def get_registro_nacional_electoral(nacionalidad: str, cedula: int):
        html = get_decoded_html(registro_electoral, nacionalidad, cedula)
        data = Selector(text=html).xpath(registro_electoral_xpath).extract()
        print(f"'{data[3]}'")
        if data[3].find("Registro") == 0:
            return CI_NO_REGISTRADA
        elif data[3] == " FALLECIDO (3)":
            print("FALLECIDO!!!!!?????")
            raise CiudadanoException(
                message=f"Error! la cedula {nacionalidad}-{cedula} pertenece a un ciudadano fallecido...",
                code=CI_FALLECIDO
            )
        pn = ParseNombre(html)
        p = Parse()
        return Ciudadano(
            nacionalidad="VENEZOLANO" if nacionalidad == "V" else "EXTRANJERO",
            cedula=nacionalidad + "-" + str(cedula),
            nombre_completo=pn.nombre_completo,
            nombres=pn.nombre_de_pila,
            apellidos=pn.apellidos,
            estado=p.parse_edo(data[data.index('Estado:') + 1]).title(),
            municipio=p.parse_mp(data[data.index('Municipio:') + 1]).title(),
            parroquia=p.parse_pq(data[data.index('Parroquia:') + 1]).title(),
            centro=p.parse_txt(data[data.index('Centro:') + 1]).title(),
            direccion=p.parse_txt(data[data.index('Dirección:') + 1]).capitalize()
        )
