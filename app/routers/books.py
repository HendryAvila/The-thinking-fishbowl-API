from  fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import Books_base, Response_books
from sql_app.database import get_db
from sql_app.models import Books
from sqlalchemy.orm import Session
from app.oauth import get_current_user
from typing import Optional

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Response_books])
async def get_all_books(db: Session = Depends(get_db),
                        current_user: int = Depends(get_current_user),
                        search: Optional[str] = "",
                        limit: int = 10,
                        offset: int = 0):
    try:
        get_all_books = db.query(Books).filter(Books.title.contains(search)).limit(limit).offset(offset).all()
        return get_all_books
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Books not found. error_ {e}")
        
    
    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Response_books)
async def create_books(book: Books_base, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        new_book = Books(**book.model_dump())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Book not created. error_ {e}")
    

@router.put("/{id}", response_model=Response_books)
async def update_book(id: int,book: Books_base, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
     update_book = db.query(Books).filter(Books.id == id)
     book_updated = update_book.first()
     update_book.update(book.model_dump(), synchronize_session=False)
     db.commit()
     return book_updated
     
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not Updated. error_ {e}")
    
@router.delete("/{id}")
async def delete_book_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        delete_book = db.query(Books).filter(Books.id == id)
        book_deleted = delete_book.first()
        delete_book.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Succesfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not Deleted. error_ {e}")
    