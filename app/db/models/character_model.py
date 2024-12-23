from app.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class CharacterModel(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    height = Column(Integer)
    mass = Column(Integer)
    hair_color = Column(String(255))
    skin_color = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(), nullable=True)

    eye_color_id = Column(Integer, ForeignKey('eye_color.id'), nullable=False)
    eye_color = relationship("EyeColorModel")
