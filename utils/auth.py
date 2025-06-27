import os
from datetime import timedelta
from datetime import datetime
from jose import jwt, JWTError
from starlette.requests import Request

ACCESS_TOKEN_EXPIRE_MINUTES=0
ALGORITHMS = "HS256"
SECRET_KEY=os.getenv("JWT_SECRET_KEY")

def create_AT(data : dict) :
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    print(f"to_encode : {to_encode}")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHMS)


def decode_AT(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMS])
        print(f"payload : {payload}")
        return payload
    except JWTError:
        return None

def get_token(request : Request) -> str:
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="인증 토큰이 없습니다.")
    return auth_header.split(" ")[1]