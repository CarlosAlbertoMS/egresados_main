from fastapi import APIRouter, Response, HTTPException
from config.db import conn
from models.role_user import role_user
from schemas.role_user import Role_user
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

role_users = APIRouter()

@role_users.get("/role_user")
def get_password_resets():
    return conn.execute(role_user.select()).mappings().fetchall()

@role_users.post("/role_user")
def create_password_resets(role_users:Role_user):
    new_role_user = { "role_id":role_users.role_id, "user_id":role_users.role_id}
    try:
        conn.execute(role_user.insert().values(new_role_user))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al insertar") 
    return JSONResponse(content=new_role_user,status_code= HTTP_200_OK)

@role_users.delete("/role_user/{id}")
def delete_role_user(id:int):
    conn.execute(role_user.delete().where(role_user.c.id == id)).mappings()
    conn.commit()
    return Response(status_code=HTTP_200_OK)