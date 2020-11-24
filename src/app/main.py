#!/usr/bin/python3
from fastapi import FastAPI, Path, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from modules.buscador import CiudadanoException, get_ciudadano
from modules.models import Ciudadano
from fastapi.openapi.utils import get_openapi


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ApiVe",
        version="2.5.0",
        description="Hecho con cariño de un programador para otro programador.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "http://apive.herokuapp.com/static/apive.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

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
def hola_a_todos():
    return {"Response": ["Hello World", "Hola Mundo" ,"Hola Venezuela"]}


@app.get("/api/v1/{nacionalidad}/{cedula}", response_model= Ciudadano)
async def buscar_ciudadano_antigua_version(nacionalidad: str, cedula: int = Path(..., title="Cedula del ciudadano", ge=1)):
    return get_ciudadano(nacionalidad.upper(), cedula)


@app.get("/v2/{nacionalidad}/{cedula}", response_model= Ciudadano)
async def buscar_ciudadano_nueva_version(nacionalidad: str, cedula: int = Path(..., title="Cedula del ciudadano", ge=1)):
    return get_ciudadano(nacionalidad.upper(), cedula)

