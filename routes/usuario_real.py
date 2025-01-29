from fastapi import APIRouter, Response, HTTPException, logger
from config.db import conn
from sqlalchemy import and_, select
from models.usuario_real import egresado, preparacion
from schemas.user import User
from fastapi.responses import JSONResponse
from fastapi import Query
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from datetime import datetime
from math import ceil


usuarios_real = APIRouter()

from sqlalchemy import func

@usuarios_real.get("/reales")
def get_usuarios(page: int = 1, per_page: int = 10):
    offset = (page - 1) * per_page

    query = (
        select(*[egresado.c, preparacion.c])
        .join(preparacion, egresado.c.preparacion_id == preparacion.c.id)
        .order_by(egresado.c.preparacion_id)
        .offset(offset)
        .limit(per_page)
    )
    result = conn.execute(query).mappings().fetchall()

    total_query = select(func.count()).select_from(egresado)
    total_count = conn.execute(total_query).scalar()

    total_pages = (total_count + per_page - 1) // per_page  # Calcular total de páginas

    return {
        "data": result,
        "total": total_count,
        "total_pages": total_pages,
        "per_page": per_page,
        "current_page": page
    }


    
@usuarios_real.get("/trabajos")
def get_usuarios_trabajo():
    query = select(egresado).where(egresado.c.primer_empleo_id.isnot(None), (egresado.c.primer_empleo_id != 0), (egresado.c.primer_empleo_id != 11) , (egresado.c.primer_empleo_id != 12) , (egresado.c.primer_empleo_id != 13)).order_by(egresado.c.primer_empleo_id)
    result =  conn.execute(query).mappings().fetchall()
    return result

from fastapi import HTTPException

@usuarios_real.post("/reales")
def create_usuarios(user: User):
    # Insertar en la tabla "preparacion"
    new_preparacion = {
        "carrera": user.carrera,
        "generacion": user.generacion,
        "fecha_inicio": user.fecha_inicio,
        "fecha_fin": user.fecha_fin,
        "promedio": user.promedio,
        "forma_titulacion": user.forma_titulacion,
        "fecha_titulo": user.fecha_titulo,
    }
    preparacion_result = conn.execute(preparacion.insert().values(new_preparacion))
    conn.commit()

    # Obtener el ID generado para "preparacion"
    preparacion_id = preparacion_result.inserted_primary_key[0]
    print(user)
    # Insertar en la tabla "egresado" usando el ID de preparación
    new_egresado = {
        "matricula": user.matricula,
        "ap_paterno": user.ap_paterno,
        "ap_materno": user.ap_materno,
        "nombres": user.nombres,
        "curp": user.curp,
        "genero": user.genero,
        "fecha_nacimiento": user.fecha_nacimiento,
        "nacionalidad": user.nacionalidad,
        "telefono": user.telefono,
        "lugar_origen": user.lugar_origen,
        "direccion_actual": user.direccion_actual,
        "imagen_url": user.imagen_url,
        "cv_url": user.cv_url,
        "habilitado": user.habilitado,
        "preparacion_id": preparacion_id,
        "primer_empleo_id": user.primer_empleo_id,
        "banderaEnc": user.banderaEnc,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    egresado_result = conn.execute(egresado.insert().values(new_egresado))
    conn.commit()
    
    if egresado_result.rowcount > 0 and preparacion_result.rowcount > 0:
        return {"egresado": new_egresado, "preparacion": new_preparacion}
    else:
        raise HTTPException(status_code=500, detail="No se pudo crear el registro.")



@usuarios_real.put("/reales/{matricula}")
def update_egresado(matricula: str, user: User):
   
    result = conn.execute(
    egresado.select().where(egresado.c.matricula == matricula)
    ).fetchone()

    # Si no se encuentra el egresado con esa matrícula, lanzar un error
    if not result:
        raise HTTPException(status_code=404, detail="Egresado no encontrado")

    # Obtener el preparacion_id usando el índice de la columna
    preparacion_id=result.preparacion_id# Accede por índice
    
    # Actualizar los datos en la tabla "preparacion" si es necesario
    updated_preparacion = {
        "carrera": user.carrera,
        "generacion": user.generacion,
        "fecha_inicio": user.fecha_inicio,
        "fecha_fin": user.fecha_fin,
        "promedio": user.promedio,
        "forma_titulacion": user.forma_titulacion,
        "fecha_titulo": user.fecha_titulo,
    }
    conn.execute(preparacion.update().where(preparacion.c.id == preparacion_id).values(updated_preparacion))
    conn.commit()

    # Actualizar los datos en la tabla "egresado" por matrícula
    updated_egresado = {
        "ap_paterno": user.ap_paterno,
        "ap_materno": user.ap_materno,
        "nombres": user.nombres,
        "curp": user.curp,
        "genero": user.genero,
        "fecha_nacimiento": user.fecha_nacimiento,
        "nacionalidad": user.nacionalidad,
        "telefono": user.telefono,
        "lugar_origen": user.lugar_origen,
        "direccion_actual": user.direccion_actual,
        "imagen_url": user.imagen_url,
        "cv_url": user.cv_url,
        "habilitado": user.habilitado,
        "primer_empleo_id": user.primer_empleo_id,
        "banderaEnc": user.banderaEnc,
        "created_at": user.created_at,
        "updated_at": datetime.now()
    }

    # Ejecutar el UPDATE en la tabla "egresado" por la matrícula
    result = conn.execute(egresado.update().where(egresado.c.matricula == matricula).values(updated_egresado))
    conn.commit()
    
    if result.rowcount > 0:
        return {"message": "Egresado actualizado con éxito.", "egresado": updated_egresado}
    else:
        raise HTTPException(status_code=404, detail="Egresado no encontrado.")
    
@usuarios_real.get('/reales/buscar')
def get_user(
    matricula: str = Query(None), 
    nombres: str = Query(None), 
    ap_paterno: str = Query(None),
    ap_materno: str = Query(None), 
    carrera: str = Query(None), 
    generacion: str = Query(None),
    page: int = Query(1, alias="page"),
    per_page: int = Query(10, alias="per_page")
):
    try:
        print(f"Parámetros recibidos: matricula={matricula}, nombres={nombres}, ap_paterno={ap_paterno}, ap_materno={ap_materno}, carrera={carrera}, generacion={generacion}, page={page}, per_page={per_page}")

        if not any([matricula, nombres, ap_paterno, ap_materno, carrera, generacion]):
            raise HTTPException(status_code=400, detail="Debe proporcionar al menos un criterio de búsqueda.")

        query = (
            select(
                egresado,
                preparacion
            )
            .select_from(
                egresado.join(preparacion, egresado.c.preparacion_id == preparacion.c.id)
            )
        )

        filters = []
        if matricula:
            filters.append(egresado.c.matricula.ilike(f"%{matricula}%"))
        if nombres:
            filters.append(egresado.c.nombres.ilike(f"%{nombres}%"))
        if ap_paterno:
            filters.append(egresado.c.ap_paterno.ilike(f"%{ap_paterno}%"))
        if ap_materno:
            filters.append(egresado.c.ap_materno.ilike(f"%{ap_materno}%"))
        if carrera:
            filters.append(preparacion.c.carrera == carrera)
        if generacion:
            filters.append(preparacion.c.generacion.ilike(f"%{generacion}%"))

        if filters:
            query = query.where(and_(*filters))

        # Obtener el total de registros sin paginación
        total_count_query = select(func.count()).select_from(query.subquery())
        total_count = conn.execute(total_count_query).scalar()

        # Calcular el total de páginas
        total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)

        # Aplicar paginación con LIMIT y OFFSET
        paginated_query = query.limit(per_page).offset((page - 1) * per_page)
        result = conn.execute(paginated_query).mappings().all()

        print(f"Total de registros encontrados: {total_count}")
        print(f"Total de páginas: {total_pages}")
        print(f"Resultados devueltos en esta página: {len(result)}")

        return {
            "total_count": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "per_page": per_page,
            "data": result
        }

    except Exception as e:
        print(f"Error interno del servidor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
