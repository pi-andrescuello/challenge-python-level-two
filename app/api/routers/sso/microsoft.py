from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from app.core.sso import oauth

class SsoMicorosftRouter:
    router = APIRouter(
        tags = ["SSO Misocorft"],
        responses = {
            404: { "description": "Not found" }
        },
    )

    @router.get('/login')
    async def login(request: Request):
        redirect_uri = request.url_for("auth_callback")
        return await oauth.microsoft.authorize_redirect(request, redirect_uri)

    
    # Callback después del login
    @router.get("/callback")
    async def auth_callback(request: Request):
        token = await oauth.microsoft.authorize_access_token(request)
        user_info = token.get("userinfo")
        if not user_info:
            raise HTTPException(status_code=400, detail="Error al obtener la información del usuario")
        
        request.session["user"] = user_info
        return RedirectResponse(url="/v1/ms/protected")  # Redirige a una página protegida

    # Función para obtener usuario autenticado
    def get_current_user(request: Request):
        user = request.session.get("user")
        if not user:
            raise HTTPException(status_code=401, detail="No autenticado")
        return user

    # Endpoint protegido
    @router.get("/protected")
    async def protected(user: dict = Depends(get_current_user)):
        return {"message": "Acceso permitido", "user": user}
    
    # Logout
    @router.get("/logout")
    async def logout(request: Request):
        request.session.pop("user", None)
        return {"message": "Sesión cerrada"}
    