from fastapi import APIRouter, Response, HTTPException
from config.db import conn
from models.password_resets import password_resets
from schemas.password_resets import Password_resets
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

password_reset = APIRouter()

@password_reset.get("/password_resets")
def get_password_resets():
    return conn.execute(password_resets.select()).mappings().fetchall()

@password_reset.post("/password_resets")
def create_password_resets(password_reset:Password_resets):
    new_password_resets = { "email":password_reset.email, "token":password_reset.token}
    try:
        conn.execute(password_resets.insert().values(new_password_resets))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al insertar") 
    return JSONResponse(content=new_password_resets,status_code= HTTP_200_OK)
