from jose import jwt,JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
SECRET_KEY="super-secret-jwt"
ALGORITHM ="HS256"
security=HTTPBearer()
def verify_token(credentials: HTTPAuthorizationCredentials= Depends(security)):
    token = credentials.credentials

    try:
        payload=jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")
    