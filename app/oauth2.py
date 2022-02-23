from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .schemas import auth_schema
from . import database, models
from .config import settings



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# Algorithm
# expiration_time

SECRETE_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(user_token: str, credentials_exception):
    try:
        payload = jwt.decode(user_token, SECRETE_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = auth_schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(user_token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Token not valid",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(user_token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user
