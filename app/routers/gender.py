from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import gender,Response_gender
from sql_app.database import get_db
from sql_app.models import Gender

router = APIRouter(
    prefix="/genders",
    tags=["gender"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_gender(gender: gender, db: Session = Depends(get_db)):
    try:
        new_gender = Gender(**gender.model_dump())
        db.add(new_gender)
        db.commit()
        db.refresh(new_gender)
        return new_gender
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Gender not created. error_ {e}")
    
@router.get("/{gender_name}", status_code=status.HTTP_200_OK)
async def get_all_gender(gender_name: str,db: Session = Depends(get_db)):
    try:
        gender = db.query(Gender).filter(Gender.gender == gender_name).first()
        gender.books
        return gender
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Gender not found. error_ {e}")    