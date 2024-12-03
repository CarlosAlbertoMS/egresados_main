from sqlalchemy import Integer,String, DateTime, Table, Column, Double, Date
from config.db import meta
from datetime import datetime
egresado = Table("egresado",meta, 
    Column("matricula", String(15), primary_key=True),
    Column("ap_paterno", String(50)),
    Column("ap_materno", String(50)),
    Column("nombres", String(100)),
    Column("curp", String(25)),
    Column("genero", String(255)),
    Column("fecha_nacimiento", DateTime),
    Column("nacionalidad", String(255)),
    Column("telefono", String(50)),
    Column("lugar_origen", String(200)),
    Column("direccion_actual", String(200)),
    Column("imagen_url", String(500)),
    Column("cv_url", String(500)),
    Column("habilitado", Integer),
    Column("preparacion_id", Integer),
    Column("primer_empleo_id", Integer),
    Column("banderaEnc", Integer),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, 
           onupdate=datetime.utcnow))

preparacion = Table("preparacion",meta,
    Column("id", Integer, primary_key = True),
    Column("carrera", Integer),
    Column("generacion", String(10)),
    Column("fecha_inicio", String(15)),
    Column("fecha_fin", String(15)),
    Column("promedio", Double),
    Column("forma_titulacion", Integer),
    Column("fecha_titulo", Date))