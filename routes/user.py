from fastapi import APIRouter, Response, HTTPException, Request
from starlette.middleware.sessions import SessionMiddleware
from config.db import conn
from models.users import users
from schemas.users import Users, Login
from passlib.hash import bcrypt
from fastapi.responses import JSONResponse
from sqlalchemy import select 
from jose import JWTError, jwt
from cryptography.fernet import Fernet
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from datetime import datetime, timedelta
import bcrypt


user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)


@user.get("/usuarios")
def get_password_resets():
    return conn.execute(users.select()).mappings().fetchall()

@user.post("/usuarios")
def create_password_resets(usuarios: Users):
    # Encriptar la contraseña
    salt = bcrypt.gensalt()  # Genera el salt automáticamente
    hashed_password = bcrypt.hashpw(usuarios.password.encode('utf-8'), salt)
    
    nuevo_usuario = {
        "correo": usuarios.correo,
        "password": hashed_password.decode('utf-8'),  # Almacenar como cadena, no bytes
        "egresado_matricula": usuarios.egresado_matricula
    }
    try:
        # Insertar el usuario en la base de datos
        conn.execute(users.insert().values(nuevo_usuario))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar: {str(e)}")

    return JSONResponse(content=nuevo_usuario, status_code=200)


@user.put("/usuarios/{id}")
def update_usuario(id: int, usuarios: Users):
    # Datos que quieres actualizar
    update_data = {}
    if usuarios.correo:
        update_data["correo"] = usuarios.correo
    if usuarios.password:
        update_data["password"] = usuarios.password

    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar.")

    try:
        # Actualización en la base de datos
        result = conn.execute(
            users.update()
            .where(users.c.id == id)
            .values(update_data)
        )
        conn.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")

    return JSONResponse(content={"message": "Usuario actualizado correctamente"}, status_code=200)

SECRET_KEY = "secretKey_"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select
import bcrypt
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Define la duración del token (puedes ajustarlo)

@user.post("/login")
def login(data: Login, request: Request):
    try:
        # Buscar al usuario por correo
        query = select(users).where(users.c.correo == data.correo)
        result = conn.execute(query).mappings().fetchone()  # Asegura que el resultado sea un mapeo (diccionario)

        if not result:
            raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

        # Verificar la contraseña usando bcrypt
        if not bcrypt.checkpw(data.password.encode("utf-8"), result["password"].encode("utf-8")):
            raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

        # Crear el token de acceso (ajusta esta función según tu implementación)
        token = create_access_token(
            data={"sub": result["correo"]}, 
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        # Responder con éxito
        return JSONResponse(
            content={
                "message": "Inicio de sesión exitoso",
                "token": token,
                "user_id": result["id"],
                "correo": result["correo"],
            },
            status_code=200,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
