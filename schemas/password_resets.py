from pydantic import BaseModel
from datetime import datetime

class Password_resets(BaseModel):
    email : str
    token : str
    created_at : datetime | Optional[datetime]= None