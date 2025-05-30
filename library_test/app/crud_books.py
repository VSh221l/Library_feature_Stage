from app.models import Book, BorrowedBook
from sqlalchemy.orm import Session
from app import schemas
from fastapi import HTTPException

def create_book(db: Session, book: schemas.BookCreate):
    """Создать новую книгу"""
    if book.isbn:
        db_book = db.query(Book).filter(Book.isbn == book.isbn).first()
        if db_book:
            raise HTTPException(status_code=400, detail="ISBN уже занят")
    
    db_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        isbn=book.isbn,
        quantity=max(book.quantity, 0)  # Гарантируем неотрицательное значение
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    """Получить книгу по ID"""
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    """Получить список всех книг"""
    return db.query(Book).offset(skip).limit(limit).all()

def get_book_by_isbn(db: Session, isbn: str):
    """Получить книгу по ISBN"""
    return db.query(Book).filter(Book.isbn == isbn).first()

def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate):
    """Обновить данные книги"""
    db_book = get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    # Проверка уникальности ISBN, если он изменен
    if book_update.isbn and book_update.isbn != db_book.isbn:
        existing = get_book_by_isbn(db, book_update.isbn)
        if existing:
            raise HTTPException(status_code=400, detail="ISBN уже занят")
    
    # Обновление полей
    for field, value in book_update.dict(exclude_unset=True).items():
        if field == "quantity" and value < 0:
            raise HTTPException(status_code=400, detail="Количество не может быть отрицательным")
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    """Удалить книгу"""
    db_book = get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Книга успешно удалена"}

def check_book_availability(db: Session, book_id: int):
    """Проверить доступность книги для выдачи"""
    book = get_book(db, book_id)
    if not book or book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Книга недоступна для выдачи")
    return book