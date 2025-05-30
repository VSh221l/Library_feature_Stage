from pydantic import BaseModel
from typing import Optional
import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: int = 1

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True

class BookCreate(BookBase):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: Optional[int] = None

class ReaderBase(BaseModel):
    name: str
    email: str

class Reader(ReaderBase):
    id: int
    class Config:
        orm_mode = True

class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class BorrowBase(BaseModel):
    book_id: int
    reader_id: int

class Borrow(BorrowBase):
    borrow_date: datetime.date
    return_date: Optional[datetime.date] = None
    return_date: Optional[str] = None
    
    class Config:
        orm_mode = True

class BorrowCreate(BorrowBase):
    pass