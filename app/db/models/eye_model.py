from app.db.base import Base
from sqlalchemy import Column, Integer, String

class EyeColorModel(Base):
    __tablename__ = "eye_color"
    id = Column(Integer, primary_key=True, index=True)
    color = Column(String(255))
