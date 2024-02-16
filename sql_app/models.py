
from sqlalchemy.orm import relationship
from sql_app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Books(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    author_name = Column(String, ForeignKey("author.name"), nullable=False)
    author = relationship("Author", back_populates="books", foreign_keys=[author_name])
    gender_name = Column(String, ForeignKey("gender.gender"), nullable=False)
    gender = relationship("Gender", back_populates="books", foreign_keys=[gender_name])
    valoration = Column(Integer, nullable=True)
    url_book = Column(String, nullable=False)
    entered_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class Author (Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    biography = Column(String, nullable=False)
    books = relationship("Books", back_populates="author")# la consulta viene aqui
    
class Gender (Base):
    __tablename__ = "gender"
    id = Column(Integer, primary_key=True, nullable=False)
    gender = Column(String, nullable=False, unique=True)
    books = relationship("Books", back_populates="gender")     
    
        
    
    
    