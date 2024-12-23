from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.character import CharacterRouter
from app.api.routers.keyphrase import KeyphraseRouter

# class for create app and send routes
class CreateApp():
    app = FastAPI()
    character_router = CharacterRouter().router
    keyphrase_router = KeyphraseRouter().router

    # contructor
    def __init__(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
            allow_headers=["*"],
        )
        self.app.include_router(self.character_router, prefix="/api")
        self.app.include_router(self.keyphrase_router, prefix="/api")
