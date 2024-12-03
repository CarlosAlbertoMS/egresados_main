from pydantic import BaseModel
from datetime import datetime

class Role_user(BaseModel):
    role_id : int
    user_id : int
    created_at : datetime
    updated_at : datetime