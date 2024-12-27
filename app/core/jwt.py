import os
from jwt import decode
from fastapi import Header, HTTPException, status

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


def verify_bearer_token(authorization: str = Header(...)):
    """
    Dependency to validate Bearer Token.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Bearer token"
        )
    
    token = authorization.split("Bearer ")[-1]
    if not auth_token(token):  # Assuming `auth_token` validates the token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return token