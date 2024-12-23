from app.db.models.character_model import CharacterModel
from app.db.models.eye_model import EyeColorModel
from app.db.base import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from app.db.models.keyphrase_model import KeyphraseModel
from app.schemas.keyphrase import KeyphraseSchema

class KeyphraseRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self):
        return self.db.query(EyeColorModel).all()

    def save(self, keyphrase: KeyphraseSchema, model: KeyphraseModel):
        if keyphrase.user_id:
            character = self.db.query(CharacterModel).filter_by(
                id=keyphrase.user_id).first()
            
            if character:
                self.db.add(model)
                self.db.commit()
                _keyphrase = model.keyphrase.split('\n- ')
                _keyphrase[0] = _keyphrase[0].replace('- ', '')

                return {
                    "user": model.user_id,
                    "user_id": character.name,
                    "keyphrase": _keyphrase
                }
    
    def get_quetions(self, user_id: int):
        return self.db.query(KeyphraseModel).filter_by(user_id=user_id).all()

