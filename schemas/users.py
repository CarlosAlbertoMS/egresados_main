from pydantic import BaseModel
from datetime import datetime

class Users(BaseModel):
    id : int | None=None
    correo : str
    password : str
    egresado_matricula : str | None = None
    remember_token:str | None=None
    created_at : datetime | None=None
    updated_at : datetime | None=None
    
class Login(BaseModel):
    correo:str
    password:str