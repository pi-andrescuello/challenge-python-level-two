from fastapi import HTTPException, status
from app.db.models.eye_model import EyeColorModel
from app.db.models.character_model import CharacterModel
from app.schemas.character import CharacterSchema
from app.schemas.keyphrase import KeyphraseSchema
from typing import List
from app.db.repository.character import CharacterRepository

class CharacterServices:
    def __init__(self, repository: CharacterRepository):
        self.repository = repository

    def get_all_characters(self) -> List[KeyphraseSchema]:
        response = self.repository.get_all()
        return response

    def get_all_colors(self):
        # Query of database in the table EyeColors
        return self.get_all_colors()

    def get_character_by_id(self, id: int):
        # Query Find Element by ID 
        model = self.repository.get_by_id(id=id)
        if model != []:
            return model
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="database or model character null"
            )

    def get_character_by_name(self, name: str):
        # Query Find Element by Name 
        model = self.repository.get_by_name(name=name)
        if model:
            return model
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="database or model character null"
            )

    def create_character(self, character: CharacterSchema):
        # Save Character in database with model
        if character.eye_color:
            model = CharacterModel(
                name=character.name,
                mass=character.mass,
                height=character.height,
                skin_color=character.skin_color,
                hair_color=character.hair_color,
                eye_color_id=character.eye_color_id,
                eye_color=EyeColorModel(
                    color=character.eye_color.color
                )
            )
            return self.repository.save(model=model)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error get characters for ID"
            )

    def delete_character(self, id: int):
        # DELETE character of the database
        model = self.repository.delete_by_id(id=id)
        if model:
            return model
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in delete model character null"
            )
    