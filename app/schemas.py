import email
from ensurepip import bootstrap
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List

class Books_base(BaseModel):
    title: str
    description: str
    author_name: str
    gender_name: str
    valoration: Optional[int]
    url_book: str
    
class Response_books(BaseModel):
    id: int
    title: str
    description: str
    author_name: str
    gender_name: str
    url_book: str
    
class Response_books_author_gender(BaseModel):
    name : str
    description: str
    
    class Config:
        from_attributes = True
        
         
    
class Create_Users(BaseModel):
    email: EmailStr
    password: str
    
class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime    
          
class TokenData(BaseModel):
    id: Optional[str] = None      
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class Author_c_u(BaseModel):
    name: str
    biography: str
    
class Response_author(BaseModel):
    id: int
    name: str
    biography: str
    books: Books_base
    class Config:
        from_attributes = True

    
class gender(BaseModel):
    gender: str
    
class Response_gender(BaseModel):
    id: int
    gender: str
    books: Response_books_author_gender
    
    class Config:
        from_attributes = True                
          