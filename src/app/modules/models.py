from pydantic import BaseModel


class Ciudadano(BaseModel):
    id: int
    nacionalidad: str
    cedula: int
    nombre_completo: str
    nombres: str
    apellidos: str
    estado: str
    municipio: str
    parroquia: str
    centro: str
    direccion: str
