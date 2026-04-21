from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "super-secret-jwt-super-secret-jwt-12345"
ALGORITHM = "HS256"

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # ✅ DO NOT CAST
        return user_id

    except JWTError as e:
        print("JWT ERROR:", e)   # 🔥 DEBUG
        raise HTTPException(status_code=401, detail="Invalid token")