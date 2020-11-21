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
