from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import Create_Users, ResponseUser
from sql_app.models import Users
from sql_app.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(
    prefix="/users",
    tags=["users"],
)




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
async def create_user(users: Create_Users, db: Session = Depends(get_db)):
    try:
        
        #hashing password
        hashed_password = pwd_context.hash(users.password)
        users.password = hashed_password
        
        new_user = Users(**users.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"User not created. error_ {e}")
    
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ResponseUser])
async def get_all_users(db: Session = Depends(get_db)):
    try:
        get_all_users = db.query(Users).all()
        return get_all_users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Users not found. error_ {e}")
    
    
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseUser)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    try:
        get_user_by_id = db.query(Users).filter(Users.id == id).first()
        return get_user_by_id
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found. error_ {e}")    
    
@router.put("/", status_code=status.HTTP_200_OK, response_model=ResponseUser)   
async def update_user(id: int, user: Create_Users, db: Session = Depends(get_db)):
    try:
        user_updated =db.query(Users).filter(Users.id == id).update(user.model_dump())
        updated_user = user_updated.first()
        user_updated.update(user.model_dump(), synchronize_session=False)
        db.commit()
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not Updated. error_ {e}")
    
@router.delete("/{id}")
async def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    try:
        delete_user = db.query(Users).filter(Users.id == id)
        user_deleted = delete_user.first()
        delete_user.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Succesfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not Deleted. error_ {e}")    
    
    