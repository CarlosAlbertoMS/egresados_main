from sqlalchemy import String, DateTime, Table, Column, Integer
from config.db import meta
from datetime import datetime
users = Table("users",meta, Column(
    "id", Integer, primary_key=True),
    Column("correo", String(50)),
    Column("password", String(255)),
    Column("egresado_matricula", String(12)),
    Column("remember_token", String(100)),
    Column("updated_at", DateTime, default=datetime.utcnow),
    Column("created_at", DateTime, default=datetime.utcnow))