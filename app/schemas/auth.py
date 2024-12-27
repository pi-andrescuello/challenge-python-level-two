from pydantic import BaseModel
from typing import Optional

class AuthSchema(BaseModel):
    id: Optional[int]
    email: str
    password: str
