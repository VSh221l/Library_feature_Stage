from app.models import Book, BorrowedBook
from sqlalchemy.orm import Session
from app import schemas
from fastapi import HTTPException
import datetime

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
    for field, value in book_update.model_dump(exclude_unset=True).items():
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

def borrow_book(db: Session, borrow: schemas.BorrowCreate):
    """Выдать книгу читателю"""
    book = check_book_availability(db, borrow.book_id)
    
    reader_borrow_count = db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == borrow.reader_id,
        BorrowedBook.return_date.is_(None)
    ).count()
    if reader_borrow_count >= 3:
        raise HTTPException(status_code=400, detail="Читатель уже взял максимальное количество книг")
    
    book.quantity -= 1
    borrow_record = BorrowedBook(**borrow.model_dump())
    db.add(borrow_record)
    db.commit()
    db.refresh(borrow_record)
    return borrow_record

def return_book(db: Session, borrow_id: int):
    borrow_record = db.query(BorrowedBook).get(borrow_id)
    if not borrow_record or borrow_record.return_date:
        raise HTTPException(status_code=400, detail="Книга уже возвращена или запись не найдена")
    
    borrow_record.return_date = datetime.datetime.now(datetime.timezone.utc)
    book = db.query(Book).get(borrow_record.book_id)
    book.quantity += 1
    
    db.commit()
    db.refresh(borrow_record)
    return borrow_record