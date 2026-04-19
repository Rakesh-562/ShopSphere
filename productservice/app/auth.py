from jose import JWTError
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()

# def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials

#     try:
#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM],
#             options={"verify_aud": False}
#         )

#         print(payload)  # debug

#         user_id = payload.get("sub")

#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         return user_id

#     except JWTError as e:
#         print("JWT ERROR:", str(e))  
#         raise HTTPException(status_code=401, detail="Invalid token")
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    print("TOKEN RECEIVED:", token) 
    print(type(token))
    print(repr(token)) # 👈 ADD THIS

    try:
        print(jwt.get_unverified_header(token))
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
          options={
                "verify_signature": True,
                "verify_aud": False   # 🔥 IMPORTANT
            }
        )

        print("PAYLOAD:", payload)  # 👈 ADD THIS

        return payload

    except JWTError as e:
        print("JWT ERROR:", str(e))  # 👈 IMPORTANT
        raise HTTPException(status_code=401, detail="Invalid token")