from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from app.db.repository.character import CharacterRepository
from app.schemas.character import CharacterSchema
from app.services.character_service import CharacterServices

class CharacterRouter:
    router = APIRouter(
        tags = ["Characters"],
        responses = {
            404: { "description": "Not found" }
        },
    )
    
    @router.get('/character/getAll', response_model=List[CharacterSchema])
    def get_all_characters(
            repository: CharacterRepository = Depends()):

        service = CharacterServices(repository)
        return service.get_all_characters()

    @router.get('/character/color/getAll')
    def get_all_colors(
            repository: CharacterRepository = Depends()):
        
        service = CharacterServices(repository)
        return service.get_all_colors()

    @router.get('/character/get/{name}')
    def get_character_by_name(
            name: str,
            repository: CharacterRepository = Depends()):
        
        service = CharacterServices(repository)
        return service.get_character_by_name(name)

    @router.get('/character/get/identify/{id}')
    def get_character_by_id(
            id: int,
            repository: CharacterRepository = Depends()):
        
        service = CharacterServices(repository)
        return service.get_character_by_id(id)

    @router.post('/character/add')
    def create_character(
            character: CharacterSchema,
            repository: CharacterRepository = Depends()):
        
        service = CharacterServices(repository)
        return service.create_character(character)

    @router.delete('/character/delete/{id}')
    def delete_character(
            id: int,
            repository: CharacterRepository = Depends()):
        
        service = CharacterServices(repository)
        return service.delete_character(id)