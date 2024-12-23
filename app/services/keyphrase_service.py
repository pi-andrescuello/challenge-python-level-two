from typing import List
from fastapi import HTTPException, status
from app.db.models.keyphrase_model import KeyphraseModel
from app.db.repository.keyphrase import KeyphraseRepository
from app.schemas.keyphrase import KeyphraseSchema
from app.services.orchestrator import Orchestrator

class KeyphraseServices:
    def __init__(self, repository: KeyphraseRepository):
        self.repository = repository

    def gpt_quetions(self, text: str) -> List[KeyphraseSchema]:
        try:
            response = Orchestrator().get_answer({"question": text})["answer"]
            response = response.split('\n- ')
            response[0] = response[0].replace('- ', '')
            return { "response": response }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: gpt quetions: {str(e)}",
            )

    def get_quetions(self, user_id: int):
        response = []
        try:
            models = self.repository.get_quetions(user_id)
            for item in models:
                new_item = item.keyphrase.split('\n- ')
                new_item[0] = new_item[0].replace('- ', '')
                response.append(new_item)
            return {"response": response }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: find gpt quetions: {str(e)}",
        )

    def gpt_post_quetions(self, keyphrase: KeyphraseSchema):
        try:
            result = Orchestrator().get_answer({"question": keyphrase.keyphrase})["answer"]
            model = KeyphraseModel(
                user_id=keyphrase.user_id,
                keyphrase=result
            )
            return self.repository.save(keyphrase, model)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: not identify in the frase: {str(e)}",
            )
        