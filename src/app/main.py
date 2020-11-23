#!/usr/bin/python3
from fastapi import FastAPI, Path, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from src.app.modules.buscador import CiudadanoException, get_ciudadano
from src.app.modules.models import Ciudadano


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(CiudadanoException)
async def unicorn_exception_handler(request: Request, exc: CiudadanoException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content= {
            "code" : exc.code,
            "message": exc.message
        }
    )

@app.get("/")
def root():
    return {"Response": ["Hello World", "Hola Mundo" ,"Hola Venezuela"]}


@app.get("/{nacionalidad}/{cedula}", response_model= Ciudadano)
def search_ciudadano_old_v(nacionalidad: str, cedula: int = Path(..., title="Cedula del ciudadano", ge=1)):
    return get_ciudadano(nacionalidad.upper(), cedula)


@app.get("/v1/{nacionalidad}/{cedula}", response_model= Ciudadano)
def search_ciudadano(nacionalidad: str, cedula: int = Path(..., title="Cedula del ciudadano", ge=1)):
    return get_ciudadano(nacionalidad.upper(), cedula)

