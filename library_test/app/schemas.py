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

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    description: Optional[str] = None
    
    class Config:
        orm_mode = True

class ReaderBase(BaseModel):
    name: str
    email: str

class ReaderCreate(ReaderBase):
    pass

class Reader(ReaderBase):
    id: int
    
    class Config:
        orm_mode = True

class BorrowBase(BaseModel):
    book_id: int
    reader_id: int

class BorrowCreate(BorrowBase):
    pass

class Borrow(BorrowBase):
    borrow_date: datetime.date
    return_date: Optional[datetime.date] = None
    return_date: Optional[str] = None
    
    class Config:
        orm_mode = True