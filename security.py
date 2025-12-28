from typing import Optional
from datetime import timedelta, datetime
from jose import jwt, JWTError
from schemas import *

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_IN_MINUTES = 30
SECRET_KEY = "11ce77236e0002c5db53a7a8b5fe417d"

def create_access_token(data:dict,expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception
        
        token_data = TokenData(username=email)

    except JWTError:
        raise credential_exception