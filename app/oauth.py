
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.schemas import TokenData
from sql_app.database import get_db
from sql_app.models import Users


SECRECT_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_TIME = settings.expiration_time

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")#h ere i take the token to pass to the funtion

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRECT_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRECT_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get("user_id"))
        if not id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="ID not found, Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(id=id) 
        
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials. error_ {e}")
        
    return token_data

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        token = verify_access_token(token)
        user_in_db = db.query(Users).filter(Users.id == token.id).first()
        if not user_in_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials, not user found",
                                headers={"WWW-Authenticate": "Bearer"})
        return user_in_db
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Could not validate credentials. error_ {e}",
                            headers={"WWW-Authenticate": "Bearer"})