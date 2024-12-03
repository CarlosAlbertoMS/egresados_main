from sqlalchemy import String, DateTime, Table, Column
from config.db import meta
from datetime import datetime
password_resets = Table("password_resets",meta, Column(
    "email", String(255)),
    Column("token", String(255)),
    Column("created_at", DateTime, default=datetime.utcnow))