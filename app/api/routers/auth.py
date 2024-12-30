from fastapi import APIRouter, Header, HTTPException, status
from app.core.jwt import auth_token
from fastapi.params import Depends
from app.schemas.user import UserSchema
from app.schemas.auth import AuthSchema
from app.db.repository.user import UserRepository
from app.services.auth_service import AuthServices

class AuthRouter:
    router = APIRouter(
        tags = ["Authentication"],
        responses = {
            404: { "description": "Not found" }
        },
    )

    @router.get('/auth')
    def get_auth(authorization: str = Header(...)):
        try:
            if not authorization or not authorization.startswith('Bearer '):
                # JWT expired return error 401
                raise HTTPException(
                    401, detail='Fail of authorization of token')

            hash_token = authorization.split(' ')[1]
            return auth_token(hash_token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"user not authenticated, details: {str(e)}"
            )

    @router.post('/auth')
    def auth(
            req: AuthSchema,
            repository: UserRepository = Depends()):
        try:
            service = AuthServices(repository)
            return service.create_auth(req)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"user not authenticated, details: {str(e)}"
            )

    @router.post('/create/user')
    def create_user(
            req: UserSchema,
            repository: UserRepository = Depends()):
        try:
            service = AuthServices(repository)
            return service.create_new_user(req)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"user not authenticated, details: {str(e)}"
            )