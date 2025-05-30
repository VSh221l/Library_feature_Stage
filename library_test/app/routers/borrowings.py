from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database
from crud import crud_books

router = APIRouter(
    prefix="/borrow",
    tags=["Borrowings"]
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
    
# 3. Получение списка всех выданных книг (идея для реализации в будущем)