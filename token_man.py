from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from schemas import TokenData
from sqlalchemy.orm import Session
from functions.user import get_user

SECRET_KEY = "4d3b3d8614c3f680eb8e3326ba6237209ccd5350f4ade42f26ac4573f289957b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# data->password expire_date->有効期限
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

def verify_token(token:str, credentials_exception, db:Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        # idをトークンから取得
        id: int = payload.get("id")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    # user情報を取得
    user = get_user(id, db)
    return user




