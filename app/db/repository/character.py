from fastapi.params import Depends
from app.db.models.character_model import CharacterModel
from app.db.models.eye_model import EyeColorModel
from app.db.base import get_db

from sqlalchemy.orm import Session

class CharacterRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def save(self, model: CharacterModel):
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model
    
    def get_colors(self):
        return self.db.query(EyeColorModel).all()
    
    def get_by_id(self, id: int):
        character = self.db.query(CharacterModel).filter_by(id=id).first()
        if character:
            eye_color = self.db.query(EyeColorModel).filter_by(
                id=character.eye_color_id).first()
            if eye_color:
                return {
                    "id": character.id,
                    "name": character.name,
                    "height": character.height,
                    "mass": character.mass,
                    "hair_color": character.hair_color,
                    "skin_color": character.skin_color,
                    "created_at": character.created_at,
                    "eye_color_id": character.eye_color_id,
                    "eye_color": {
                        "id": eye_color.id,
                        "color": eye_color.color
                    }
                }
        else: 
            return []

    def get_by_name(self, name: str):
        character = self.db.query(CharacterModel).filter_by(name=name).first()
        if character:
            eye_color = self.db.query(EyeColorModel).filter_by(
                id=character.eye_color_id).first()
            if eye_color:
                return {
                    "id": character.id,
                    "name": character.name,
                    "height": character.height,
                    "mass": character.mass,
                    "hair_color": character.hair_color,
                    "skin_color": character.skin_color,
                    "created_at": character.created_at,
                    "eye_color_id": character.eye_color_id,
                    "eye_color": {
                        "id": eye_color.id,
                        "color": eye_color.color
                    }
                }
        else: 
            return []

    def get_all(self):
        characters_with_eye_color = []
        characters = self.db.query(CharacterModel).all()

        if characters:
            for character in characters:
                eye_color = self.db.query(EyeColorModel).filter_by(
                    id=character.eye_color_id).first()
                if eye_color:
                    character_with_eye_color = {
                        "id": character.id,
                        "name": character.name,
                        "height": character.height,
                        "mass": character.mass,
                        "hair_color": character.hair_color,
                        "skin_color": character.skin_color,
                        "created_at": character.created_at,
                        "eye_color_id": character.eye_color_id,
                        "eye_color": {
                            "id": eye_color.id,
                            "color": eye_color.color
                        }
                    }
                    characters_with_eye_color.append(
                        character_with_eye_color)
        return characters_with_eye_color

    def delete_by_id(self, id: int):
        character = self.db.query(CharacterModel).filter_by(
            id=id).first()
        if character:
            eye_color = self.db.query(EyeColorModel).filter_by(
                id=character.eye_color_id).first()
            
            if eye_color:
                self.db.delete(character)
                self.db.delete(eye_color)
                self.db.commit()
            return character
        else: 
            return []