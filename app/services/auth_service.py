from fastapi import HTTPException, status
import os
import bcrypt

from jwt import encode
from fastapi import HTTPException, status
from app.core.bcrypt import hash_password
from app.db.models.user_model import UserModel
from app.db.repository.user import UserRepository

class AuthServices:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_auth(self, req):
        '''
        Query for Add in the table UserModel database
        '''
        if req:
            user = self.repository.get_user_by_email(email=req.email)
            if user:
                if not bcrypt.checkpw(
                    req.password.encode('utf-8'), user.password.encode('utf-8')
                ):
                    raise HTTPException(401, detail="passwords do not match")

                token = encode({
                    'user': {
                        'id': user.id,
                        'role': user.role,
                        'email': user.email
                    }
                }, os.getenv('JWT_SECRET'), algorithm='HS256')
            return {'x-auth-token': token}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                detail="database or model user null")
    
    def create_new_user(self, req):
        # Query for Add in the table UserModel database
        if req:
            model = UserModel(
                email=req.email,
                role=req.role,
                first_name=req.first_name,
                last_name=req.last_name,
                user_name=req.user_name,
                password=hash_password(req.password),
            )
            return self.repository.save(model)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="database or model user null"
            )