import os
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv

load_dotenv()

# Configurar OAuth2 con Microsoft
oauth = OAuth()
oauth.register(
    name="microsoft",
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET_VALUE"),
    authorize_url=f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/authorize",
    token_url=f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/token",
    access_token_url=f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/token",
    jwks_uri="https://login.microsoftonline.com/common/discovery/v2.0/keys",
    userinfo_endpoint="https://graph.microsoft.com/oidc/userinfo",
    redirect_uri=f"{os.getenv('URL_WEBAPP')}auth/callback",
    client_kwargs={"scope": "openid profile email"},
)
