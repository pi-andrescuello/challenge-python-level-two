from fastapi import FastAPI
from app.api.routers import auth, client, example, external_services

def create_app():
    app = FastAPI()
    
    app.include_router(auth.router, prefix="/api")
    app.include_router(client.router, prefix="/api")
    app.include_router(example.router, prefix="/api")
    app.include_router(external_services.router, prefix="/api")

    return app