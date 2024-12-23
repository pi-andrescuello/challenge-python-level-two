from fastapi import APIRouter
from fastapi.params import Depends
from app.db.repository.keyphrase import KeyphraseRepository
from app.schemas.keyphrase import KeyphraseSchema
from app.services.keyphrase_service import KeyphraseServices

class KeyphraseRouter:
    router = APIRouter(
        tags = ["Keyphrase"],
        responses = {
            404: { "description": "Not found" }
        },
    )
    
    @router.get('/keyphrase/{text}')
    def gpt_quetions(
            text: str,
            repository: KeyphraseRepository = Depends()):
        
        service = KeyphraseServices(repository)
        return service.gpt_quetions(text)

    @router.get('/keyphrase/character_id/{user_id}')
    def gpt_find_quetions(
            user_id: str,
            repository: KeyphraseRepository = Depends()):

            service = KeyphraseServices(repository)
            return service.get_quetions(user_id)

    @router.post('/keyphrase')
    def gpt_post_quetions(
            model: KeyphraseSchema,
            repository: KeyphraseRepository = Depends()):

            service = KeyphraseServices(repository)
            return service.gpt_post_quetions(model)