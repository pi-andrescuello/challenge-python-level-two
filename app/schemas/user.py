from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    user_name: str
    password: str
    role: Optional[int]
