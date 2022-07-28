#!/usr/bin/python3
from databases import Database
from fastapi import FastAPI, Path, Request, status
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseSettings
from sqlalchemy import Column, MetaData, Table, create_engine
from sqlalchemy.sql import select
from sqlalchemy.sql.sqltypes import Integer, String
from starlette.middleware.cors import CORSMiddleware

from modules.buscador import Buscar, CiudadanoException
from modules.models import Ciudadano


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
        "url": "https://apive.herokuapp.com/static/apive.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


class Settings(BaseSettings):
    app_name: str = "ApiVe"
    admin_email: str
    items_per_user: int = 50


app = FastAPI()
settings = Settings(
    app_name = "ApiVe",
    admin_email="vikruzdavid@gmail.com",
)
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
metadata = MetaData()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.openapi = custom_openapi


ciudadanos = Table(
    "ciudadanos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nacionalidad", String),
    Column("cedula", Integer, unique=True),
    Column("nombre_completo", String),
    Column("nombres", String),
    Column("apellidos", String),
    Column("estado", String),
    Column("municipio", String),
    Column("parroquia", String),
    Column("centro", String),
    Column("direccion", String),
)
engine = create_engine(
    DATABASE_URL
)
metadata.create_all(engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }


async def insertar_ciudadano(ciudadano: Ciudadano):
    query = ciudadanos.insert().values(
        nacionalidad=ciudadano.nacionalidad,
        cedula=ciudadano.cedula,
        nombre_completo=ciudadano.nombre_completo,
        nombres=ciudadano.nombres,
        apellidos=ciudadano.apellidos,
        estado=ciudadano.estado,
        municipio=ciudadano.municipio,
        parroquia=ciudadano.parroquia,
        centro=ciudadano.centro,
        direccion=ciudadano.direccion,
    )
    last_record_id = await database.execute(query)
    return {**ciudadano.dict(), "id": last_record_id}


@app.exception_handler(CiudadanoException)
async def unicorn_exception_handler(request: Request, exc: CiudadanoException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": exc.code,
            "message": exc.message
        }
    )

@app.get("/")
async def home_page():
    return HTMLResponse(status_code=status.HTTP_200_OK, content=open("index.html", "r").read())
    
    

@app.get("/api/v1/{nacionalidad}/{cedula}", response_model=Ciudadano)
async def buscar_ciudadano(nacionalidad: str, cedula: int = Path(..., title="Cedula del ciudadano", ge=1)):
    var = select([ciudadanos]).where(ciudadanos.c.cedula == cedula)
    sqlite_local = await database.fetch_one(query=var)
    if sqlite_local is not None:
        return Ciudadano(
            id=sqlite_local[0],
            nacionalidad=sqlite_local[1],
            cedula=sqlite_local[2],
            nombre_completo=sqlite_local[3],
            nombres=sqlite_local[4],
            apellidos=sqlite_local[5],
            estado=sqlite_local[6],
            municipio=sqlite_local[7],
            parroquia=sqlite_local[8],
            centro=sqlite_local[9],
            direccion=sqlite_local[10]
        )
    ciudadano = Buscar(
    nacionalidad=nacionalidad,
    cedula=cedula)
    tmp = ciudadano.get_ciudadano()
    return await insertar_ciudadano(tmp)
