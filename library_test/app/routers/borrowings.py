from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database, auth
from app.crud import crud_books

router = APIRouter(
    prefix="/borrow",
    tags=["Borrowings"],
    dependencies=[Depends(auth.get_current_user)]  # Все эндпоинты требуют JWT
)


# --- Выдача и возврат книг ---

# 1. Выдача книги читателю
@router.post("/", response_model=schemas.Borrow)
def borrow_book(borrow: schemas.BorrowCreate, db: Session = Depends(database.get_database)):
    try:
        return crud_books.borrow_book(db, borrow)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 2. Возврат книги
@router.post("/return", response_model=dict)
def return_book(borrow_id: int, db: Session = Depends(database.get_database)):
    try:
        return crud_books.return_book(db, borrow_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# 3. Получение списка книг, взятых читателем
@router.get("/reader/{reader_id}", response_model=list[schemas.Borrow])
def get_reader_borrowed_books(reader_id: int, db: Session = Depends(database.get_database)):
    return crud_books.get_reader_borrowed_books(db, reader_id)