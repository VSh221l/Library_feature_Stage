from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer)
    isbn = Column(String, unique=True, nullable=True)
    quantity = Column(Integer, default=1)
    description = Column(String, nullable=True)  # Добавлено через Alembic
    
class Reader(Base):
    __tablename__ = "readers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

class BorrowedBook(Base):
    __tablename__ = "borrowed_books"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    borrow_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    return_date = Column(DateTime, nullable=True)
    
    book = relationship("Book")
    reader = relationship("Reader")