import  urllib.request

class ConsultarDatos():
    """
    Clase que se encarga de conectarnos con los servicios de internet.
    """
    url_base_cne = 'http://www.cne.gov.ve/web/registro_'
    url_registro_civil = 'civil/buscar_rep.php?nacionalidad='
    url_cne = 'electoral/ce.php?nacionalidad='
    nacionalidad = str
    cedula = int
    def __init__(self, nacionalidad: str, cedula: int):
        """Constructor ejemplo: ConsultarDatos("V", 12345678)

        Args:
            nacionalidad (str): [Nacionalidad a consultar]
            cedula (int): [Cedula a consultar]
        """        
        self.nacionalidad = nacionalidad
        self.cedula = cedula

    def _get_decoded_html(self, url: str):
        """Este metodo se conecta a internet usando urllib 
        retornando html limpio y decodificado en utf-8.

        Args:
                url (str): Url a conectar

        Returns:
                str: html decodificado
        """
        print(url)
        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req) as response:
                the_page = response.read().decode('utf8')
            return str(the_page.replace('\t', '').replace('\n', '').replace('\r', ''))
        except Exception as x:
            print('Fallo la conexion :(', x.__class__.__name__)
            raise x


    def registro_nacional_electoral(self):
        """[Obtiene el html limpio de la web del cne]
        
        Returns:
            [str]: [html limpio de la web del cne]
        """
        url_de_consulta = f"{self.url_base_cne}{self.url_cne}{self.nacionalidad}&cedula={self.cedula}"
        return self._get_decoded_html(url_de_consulta)

    def registro_civil(self):
        """[Obtiene el html limpio del registro civil]

        Returns:
            [str]: [html limpio del registro civil]
        """        
        url_de_consulta = f"{self.url_base_cne}{self.url_registro_civil}{self.nacionalidad}&ced={self.cedula}"
        return self._get_decoded_html(url_de_consulta)
