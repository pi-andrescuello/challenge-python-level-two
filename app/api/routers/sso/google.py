import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import google_auth_oauthlib.flow
from dotenv import load_dotenv

load_dotenv()

# Configuración de Google OAuth
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
URL_WEBAPP = os.getenv("URL_WEBAPP")

REDIRECT_URI = f"{URL_WEBAPP}v1/gl/callback"
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
]


class SsoGoogleRouter:
    router = APIRouter(
        tags = ["SSO Google"],
        responses = {
            404: { "description": "Not found" }
        },
    )

    @router.get('/login')
    async def login(request: Request):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            {
                "web": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uris": [REDIRECT_URI],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
        )
        flow.redirect_uri = REDIRECT_URI
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        
        request.session["state"] = state  # Guardar el state en la sesión
        return RedirectResponse(url=authorization_url)

    
    # Callback después del login
    @router.get("/callback")
    def auth_callback(request: Request):
        code = request.query_params.get("code")
        state = request.query_params.get("state")  # Obtener state de la URL
        stored_state = request.session.get("state")  # Obtener state guardado

        if not code:
            return {"error": "No authorization code found"}
        
        if state != stored_state:
            return {"error": "State mismatch, possible CSRF attack"}

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            {
                "web": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uris": [REDIRECT_URI],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
            state=state,  # Pasar el state almacenado
        )
        flow.redirect_uri = REDIRECT_URI

        try:
            flow.fetch_token(
                authorization_response=str(request.url)
            )
        except Exception as e:
            print("Error fetching token:", e)
            return {"error": "Failed to fetch token"}

        credentials = flow.credentials
        return {"access_token": credentials.token}