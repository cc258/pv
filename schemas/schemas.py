from pydantic import BaseModel
from datetime import datetime

class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    email: str
    created_at: datetime|None = None
    updated_at: datetime|None = None