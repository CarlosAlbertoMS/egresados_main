from sqlalchemy import Integer,String, DateTime, Table, Column
from config.db import meta
from datetime import datetime
role_user = Table("role_user",meta, 
    Column("id", Integer, primary_key=True),
    Column("role_id", Integer),
    Column("user_id", Integer),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default = datetime.utcnow))