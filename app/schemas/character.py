from pydantic import BaseModel
from typing import Optional
from app.schemas.eye_color import eye_color_schema

class CharacterSchema(BaseModel):
    id: int
    name: str
    height: float
    mass: float
    hair_color: str
    skin_color: str
    eye_color_id: Optional[int]
    eye_color: eye_color_schema
