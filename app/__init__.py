import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routers.auth import AuthRouter
from app.api.routers.sso.google import SsoGoogleRouter
from app.api.routers.sso.microsoft import SsoMicorosftRouter
from app.api.routers.character import CharacterRouter
from app.api.routers.keyphrase import KeyphraseRouter
from starlette.middleware.sessions import SessionMiddleware

# class for create app and send routes
class CreateApp():
    app = FastAPI()
    
    sso_micorosft_router = SsoMicorosftRouter().router
    sso_google_router = SsoGoogleRouter().router
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


        @self.app.exception_handler(Exception)
        async def custom_exception_handler(request: Request, exc: Exception):
            response = JSONResponse(
                content={"error": "Internal Server Error"},
                status_code=500, 
                headers={
                    "Content-Type": "application/json",
                    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
                    "X-Frame-Options": "SAMEORIGIN",
                    "X-Content-Type-Options": "nosniff",
                    "Referrer-Policy": "no-referrer",
                    "Permissions-Policy": "geolocation=(), microphone=()",
                    "Content-Security-Policy": "default-src 'self'"
                }
            )
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["X-Frame-Options"] = "SAMEORIGIN"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["Referrer-Policy"] = "no-referrer"
            response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
            response.headers["Content-Security-Policy"] = "default-src 'self'"
            return response

        # Middleware de autenticación
        @self.app.middleware("http")
        async def check_authentication(request: Request, call_next):
            try:
                response = await call_next(request)
                response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
                response.headers["Content-Security-Policy"] = "default-src 'self'"
                response.headers["X-Frame-Options"] = "SAMEORIGIN"
                response.headers["X-Content-Type-Options"] = "nosniff"
                response.headers["Referrer-Policy"] = "no-referrer"
                response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
                return response
            except Exception as e:
                import traceback
                print("Error en autenticación:", str(e))
                print(traceback.format_exc())
                return JSONResponse(
                    status_code=500, 
                    content={"error": "Internal Server Error"}, 
                    headers={
                        "Content-Type": "application/json",
                        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
                        "X-Frame-Options": "SAMEORIGIN",
                        "X-Content-Type-Options": "nosniff",
                        "Referrer-Policy": "no-referrer",
                        "Permissions-Policy": "geolocation=(), microphone=()",
                        "Content-Security-Policy": "default-src 'self'"
                    }
                )

        self.app.include_router(self.sso_micorosft_router, prefix="/v1/ms")
        self.app.include_router(self.sso_google_router, prefix="/v1/gl")
        self.app.include_router(self.auth_router, prefix="/api")
        self.app.include_router(self.character_router, prefix="/api")
        self.app.include_router(self.keyphrase_router, prefix="/api")
