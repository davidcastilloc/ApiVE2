from pydantic import BaseModel


class Ciudadano(BaseModel):
    nacionalidad: str
    cedula: str
    nombre: str
    estado: str
    municipio: str
    parroquia: str
    centro: str
    direccion: str
