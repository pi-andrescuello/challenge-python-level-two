import os
from jwt import decode
from fastapi import Header, HTTPException, status
from typing import Optional

# This is Roles for User
class UsersRole:
    USER = 0
    ADMIN = 1

USER_ROLE = UsersRole()


# Validation JWT in case expired [ UserModel or 401 ]
def auth_token(authorization):
    if not authorization:
        # JWT expired return error 401
        raise HTTPException(
            401, detail='Fail of authorization of token')

    result = decode(authorization, os.getenv(
        'JWT_SECRET'), algorithms=['HS256'])

    # Return object user with dates of schema UserModel
    return result.get('user')


# Function for verify Tokens
def verify_bearer_token(
    authorization: Optional[str] = Header(default=None), 
    required_roles: Optional[list[int]] = None
):
    """
    Dependency to validate Bearer Token and roles.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Bearer token"
        )
    
    token = authorization.split("Bearer ")[-1]
    user_data = auth_token(token)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    if required_roles and user_data.get("role") not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    
    return user_data


def verify_user_or_admin_token(authorization: str = Header(default=None)):
    return verify_bearer_token(authorization=authorization, required_roles=[USER_ROLE.USER, USER_ROLE.ADMIN])


def verify_admin_token(authorization: str = Header(default=None)):
    return verify_bearer_token(authorization=authorization, required_roles=[USER_ROLE.ADMIN])