from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, database, auth
from crud import crud_books

# Создаем роутер для книг
router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(auth.get_current_user)]  # Все эндпоинты требуют JWT
)

# --- CRUD для книг ---

# 1. Создание книги
@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_database)):
    return crud_books.create_book(db, book)

# 2. Получение всех книг (публичный эндпоинт)
@router.get("/", response_model=list[schemas.Book], tags=["Public"])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_database)):
    return crud_books.get_books(db, skip=skip, limit=limit)

# 3. Получение книги по ID
@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(database.get_database)):
    db_book = crud_books.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return db_book

# 4. Обновление книги
@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(database.get_database)):
    db_book = crud_books.update_book(db, book_id, book_update)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return db_book

# 5. Удаление книги
@router.delete("/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(database.get_database)):
    result = crud_books.delete_book(db, book_id)
    return result