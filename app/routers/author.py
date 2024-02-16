from turtle import title
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Author_c_u, Response_author, Books_base
from sql_app.database import get_db
from sql_app.models import Author

router = APIRouter(
    prefix="/author",
    tags=["author"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_author(author: Author_c_u, db: Session = Depends(get_db)):
    try:
        new_author = Author(**author.model_dump())
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        return new_author
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Author not created. error_ {e}")
    
@router.get("/{author_name}", status_code=status.HTTP_200_OK)
async def get_author_by_id(author_name: str, db: Session = Depends(get_db)):
    try:
        author = db.query(Author).filter(Author.name == author_name).first()
        author.books# me guardo los libros aqui
        return author
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author not found. error_ {e}")