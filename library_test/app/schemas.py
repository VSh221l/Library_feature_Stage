from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
import datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(UserLogin):
    pass  # Регистрация использует те же поля, что и вход

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: int = 1

class Book(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class BorrowBase(BaseModel):
    book_id: int
    reader_id: int

class Borrow(BorrowBase):
    id: int
    borrow_date: datetime.datetime
    return_date: Optional[datetime.datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class BorrowCreate(BorrowBase):
    pass