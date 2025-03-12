import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routers.auth import AuthRouter
from app.api.routers.sso import SSORouter
from app.api.routers.character import CharacterRouter
from app.api.routers.keyphrase import KeyphraseRouter
from starlette.middleware.sessions import SessionMiddleware

# class for create app and send routes
class CreateApp():
    app = FastAPI()
    
    sso_router = SSORouter().router
    auth_router = AuthRouter().router
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
        # Middleware para manejar sesiones
        self.app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", ""))

        # Middleware de autenticación
        @self.app.middleware("http")
        async def check_authentication(request: Request, call_next):
            try:
                return await call_next(request)
            except Exception as e:
                import traceback
                print("Error en autenticación:", str(e))
                print(traceback.format_exc())
                return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

        self.app.include_router(self.sso_router, prefix="/auth")
        self.app.include_router(self.auth_router, prefix="/api")
        self.app.include_router(self.character_router, prefix="/api")
        self.app.include_router(self.keyphrase_router, prefix="/api")
