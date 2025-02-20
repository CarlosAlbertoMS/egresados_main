from fastapi import APIRouter, Response, HTTPException, FastAPI
from config.db import conn
from sqlalchemy import select
from fastapi.middleware.cors import CORSMiddleware
from models.empleador import empleador
from schemas.empleador import Empleador
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
import logging

# Configurar el logger
logging.basicConfig(level=logging.DEBUG)

empleadores = APIRouter()
app = FastAPI()

@empleadores.post("/empleadores")
def create_empleador(empleado: Empleador):
    new_empleador = {
        "nombre_empresa": empleado.nombre_empresa,
        "nombre_jefe": empleado.nombre_jefe,
        "correo": empleado.correo,
        "puesto": empleado.puesto,
        "telefono": empleado.telefono,
        "licenciatura_posgrado": empleado.licenciatura_posgrado,
        "puesto_egresado": empleado.puesto_egresado,
        "antiguedad": empleado.antiguedad,
        "uno": empleado.uno,
        "dosa": empleado.dosa,
        "dosb": empleado.dosb,
        "tresa": empleado.tresa,
        "tresb": empleado.tresb,
        "cuatroa": empleado.cuatroa,
        "cuatrob": empleado.cuatrob,
        "cuatroc": empleado.cuatroc,
        "cuatrod": empleado.cuatrod,
        "cuatroe": empleado.cuatroe,
        "cuatrof": empleado.cuatrof,
        "cinco": empleado.cinco,
        "seisa": empleado.seisa,
        "seisb": empleado.seisb,
        "sietea": empleado.sietea,
        "sieteb": empleado.sieteb,
        "sietec": empleado.sietec,
        "sieted": empleado.sieted,
        "sietee": empleado.sietee,
        "sietef": empleado.sietef,
        "ocho": empleado.ocho,
        "nuevea": empleado.nuevea,
        "nueveb": empleado.nueveb,
        "nuevec": empleado.nuevec,
        "nueved": empleado.nueved,
        "nuevee": empleado.nuevee,
        "nuevef": empleado.nuevef,
        "nueveg": empleado.nueveg,
        "dieza": empleado.dieza,
        "diezb": empleado.diezb,
        "diezc": empleado.diezc,
        "diezd": empleado.diezd,
        "dieze": empleado.dieze,
        "diezf": empleado.diezf,
        "oncea": empleado.oncea,
        "onceb": empleado.onceb,
        "doce": empleado.doce
    }
    empleador_result = conn.execute(empleador.insert().values(new_empleador))
    conn.commit()
    
    if empleador_result.rowcount > 0:
        return {"empleador": new_empleador}
    else:
        raise HTTPException(status_code=500, detail="No se pudo crear el registro.")
