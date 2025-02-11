from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Users(BaseModel):
    id : int | Optional[int]= None
    correo : str
    password : str
    egresado_matricula : str | Optional[str]= None
    remember_token:str | Optional[str]= None
    created_at : datetime | Optional[datetime]= None
    updated_at : datetime | Optional[datetime]= None
    
class Login(BaseModel):
    correo:str
    password:str