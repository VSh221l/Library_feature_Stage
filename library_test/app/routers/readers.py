from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, database, auth
from crud import crud_readers

# Создаем роутер для читателей
router = APIRouter(
    prefix="/readers",
    tags=["Readers"],
    dependencies=[Depends(auth.get_current_user)]  # Все эндпоинты требуют JWT
)

# --- CRUD для читателей ---

# 1. Создание читателя
@router.post("/", response_model=schemas.Reader, status_code=status.HTTP_201_CREATED)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(database.get_database)):
    return crud_readers.create_reader(db, reader)

# 2. Получение всех читателей
@router.get("/", response_model=list[schemas.Reader])
def read_readers(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_database)):
    return crud_readers.get_readers(db, skip=skip, limit=limit)

# 3. Получение читателя по ID
@router.get("/{reader_id}", response_model=schemas.Reader)
def read_reader(reader_id: int, db: Session = Depends(database.get_database)):
    db_reader = crud_readers.get_reader(db, reader_id)
    if not db_reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return db_reader

# 4. Обновление читателя
@router.put("/{reader_id}", response_model=schemas.Reader)
def update_reader(reader_id: int, reader_update: schemas.ReaderUpdate, db: Session = Depends(database.get_database)):
    db_reader = crud_readers.update_reader(db, reader_id, reader_update)
    if not db_reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return db_reader

# 5. Удаление читателя
@router.delete("/{reader_id}", response_model=dict)
def delete_reader(reader_id: int, db: Session = Depends(database.get_database)):
    result = crud_readers.delete_reader(db, reader_id)
    return result