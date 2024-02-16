from fastapi import APIRouter, Depends, HTTPException, status
from sql_app.models import Users
from sql_app.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.oauth import create_access_token, get_current_user
from app.schemas import Token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/login",
)

@router.post("/", status_code=status.HTTP_202_ACCEPTED,response_model=Token)
async def login_user(user_login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.email == user_login.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
        if not pwd_context.verify(user_login.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    #create the acces token 
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    
   
