from app.db.base import Base
from sqlalchemy import Column, Integer, Text

# EyeColorModel implementation
class KeyphraseModel(Base):
    __tablename__ = "keyphrase"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    keyphrase = Column(Text, default="", nullable=False)
