#!/usr/bin/python3
from fastapi import FastAPI, HTTPException, Path, status
from starlette.middleware.cors import CORSMiddleware
from .models import Ciudadano
from .Ciudadano import get_ciudadano

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/v1/{nacionalidad}/{cedula}", status_code=status.HTTP_200_OK)
def search_ciudadano(nacionalidad: str, cedula: int = Path(..., title="Cedula del ciudadano", ge=1)):
    response = get_ciudadano(nacionalidad.upper(), int(cedula))
    return response
