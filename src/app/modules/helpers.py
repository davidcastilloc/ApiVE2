from typing import List

from scrapy.selector import Selector


class Parse(object):
    replace_ci = ['.', ',', ' ']

    replace_edo = {'Edo. ': '', 'Dtto. Capital': 'Distrito Capital'}

    replace_mp = {'Mp. ': '', 'Ce. Blvno Libertador': 'Libertador', 'Ce. ': '',
                  'Mp.': '', }

    replace_pq = {'Pq. ': '', 'Cm. ': ''}

    replace_txt = {
        '\xc3\x83\xc2\x93': '\xc3\xb3',  # ó
        '\xc3\x83\xc2\x8d': '\xc3\xad',  # í
        '\xc3\x90': 'ñ',  # ñ
        '\xf1': 'ñ', ''
                     'Á': 'a', 'á': 'a', 'À': 'a', 'à': 'a', 'Ä': 'a', 'ä': 'a',
        'É': 'e', 'é': 'e', 'È': 'e', 'è': 'e', 'Ë': 'e', 'ë': 'e',
        'Í': 'i', 'í': 'i', 'Ì': 'i', 'ì': 'i', 'Ï': 'i', 'ï': 'i',
        'Ó': 'o', 'ó': 'o', 'Ò': 'o', 'ò': 'o', 'Ö': 'o', 'ö': 'o',
        'Ú': 'u', 'ú': 'u', 'Ù': 'u', 'ù': 'u', 'Ü': 'u', 'ü': 'u'
    }

    @staticmethod
    def parse_data(diccionario, data):
        for to_replace, new in diccionario.items():
            data = data.replace(to_replace, new, 1)
        return data

    @classmethod
    def parse_txt(cls, data):
        return cls.parse_data(cls.replace_txt, data)

    @classmethod
    def parse_edo(cls, data):
        return cls._parse_edo(cls.parse_txt(data).title())

    @classmethod
    def parse_mp(cls, data):
        return cls._parse_mp(cls.parse_txt(data).title())

    @classmethod
    def parse_pq(cls, data):
        return cls._parse_pq(cls.parse_txt(data).title())

    @classmethod
    def _parse_edo(cls, data):
        return cls.parse_data(cls.replace_edo, data)

    @classmethod
    def _parse_mp(cls, data):
        return cls.parse_data(cls.replace_mp, data)

    @classmethod
    def _parse_pq(cls, data):
        return cls.parse_data(cls.replace_pq, data)


class ParseNombre:
    nombre_de_pila = str
    apellidos = str
    nombre_completo = str
    html_data = None

    def __init__(self, decoded_html=str):
        # primero tomar la decicion
        if decoded_html is not None:
            self.html_data = Selector(text=decoded_html, type="html").xpath("//b")
            print(self.html_data)
            if decoded_html.find("REGISTRO ELECTORAL - CONSULTA DE DATOS") > 0:
                self._extraer_nombre_html_cne()
            else:
                self._calc_nombre(self.html_data.extract_first())
            print("resultado de funcion")
            print(self.nombre_de_pila)
            print(self.apellidos)
            print(self.nombre_completo)
            self.nombre_de_pila = self.nombre_de_pila.title()
            self.apellidos = self.apellidos.title()
            self.nombre_completo = self.nombre_completo.title()

    def _extraer_nombre_html_cne(self):
        nombre_html = self.html_data[3].extract()
        self._calc_nombre(nombre_html)

    def _extraer_nombre_html_registro_civil(self):
        nombre_html = self.html_data[3].extract()
        self._calc_nombre(nombre_html)

    def _calc_nombre(self, nombre_html_de_scrapy):
        self.nombre_completo = nombre_html_de_scrapy.replace('</b>', '').replace('<b>', '')
        nombre = self.nombre_completo.split()
        # si el ciudadano tiene un solo apellido devuelve True
        un_apellido_test = nombre_html_de_scrapy.find(' </b>') > 0
        # si el ciudadano tiene un solo nombre devuelve True
        un_nombre_test = nombre_html_de_scrapy.find('  ') > 0
        print(un_apellido_test)
        print(un_nombre_test)
        if len(nombre) == 4:
            self.nombre_de_pila = f"{nombre[0]} {nombre[1]}"
            self.apellidos = f"{nombre[-2]} {nombre[-1]}"
        elif len(nombre) == 3:
            if un_apellido_test:
                self.nombre_de_pila = f"{nombre[0]} {nombre[1]}"
                # obtenemos el apellido apuntando al ultimo item -1
                self.apellidos = nombre[-1]
            if un_nombre_test:
                # COLOCAMOS LOS NOMBRES Y APELLIDOS DONDE VAN
                self.nombre_de_pila = f"{nombre[0]} {nombre[1]}"
                self.apellidos = f"{nombre[1]} {nombre[2]}"
        elif len(nombre) == 2:
            self.nombre_de_pila = f"{nombre[0]}"
            self.apellidos = nombre[-1]
        elif len(nombre) == 5:
            self.nombre_de_pila = f"{nombre[0]} {nombre[1]} {nombre[2]}"
            self.apellidos = f"{nombre[-2]} {nombre[-1]}"
        elif nombre == "DE" or nombre == "DEL" in nombre:
            conectivos = []
            for k, v in enumerate(nombre):
                if v == "DE" or v == "DEL":
                    decision = len(nombre) / 2
                    if k <= decision:
                        print("CONECTIVO INICIO ENCONTRADO >" + v)
                        print(f"{k} {v}")
                        conectivos.append([k, v])
                        offset = k + 1
                        self.nombre_de_pila = f"{nombre[0]} {nombre[offset - 1]} {nombre[offset]}"
                        self.apellidos = nombre[-1]
                    else:
                        print("CONECTIVO FINAL ENCONTRADO >" + v)
                        print(f"{k} {v}")
                        conectivos.append([k, v])
                        self.nombre_de_pila = f"{nombre[0]} {nombre[1]}"
                        self.apellidos = f"{nombre[-3]} {conectivos[0][1]} {nombre[conectivos[0][0] + 1]}"
            if len(conectivos) > 1:
                print("HAY MAS DE 1 CONECTIVO> ")
                print(conectivos)
                self.nombre_de_pila = f"{nombre[0]} {nombre[1]} {nombre[2]}"
                self.apellidos = f"{nombre[-3]} {conectivos[-1][1]} {nombre[-1]}"
