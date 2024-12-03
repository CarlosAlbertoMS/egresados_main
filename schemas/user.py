from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    matricula : str | None=None
    ap_paterno: str
    ap_materno: str
    nombres: str
    curp: str
    genero: str
    fecha_nacimiento: Optional[datetime]= None
    nacionalidad: str
    telefono: str
    lugar_origen: str
    direccion_actual: str
    imagen_url: str
    cv_url: str
    habilitado: int
    preparacion_id: Optional[int] = None
    primer_empleo_id: Optional[int] = None
    banderaEnc: int
    carrera: int
    generacion: str
    fecha_inicio: str
    fecha_fin: str
    promedio: float
    forma_titulacion: int
    fecha_titulo: Optional[datetime] = None
    created_at: Optional[datetime]= None
    updated_at: Optional[datetime]= None