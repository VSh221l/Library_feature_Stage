from app.models import Reader
from sqlalchemy.orm import Session
from app import schemas
from fastapi import HTTPException

def create_reader(db: Session, reader: schemas.ReaderCreate):
    """Создать нового читателя"""
    db_reader = db.query(Reader).filter(Reader.email == reader.email).first()
    if db_reader:
        raise HTTPException(status_code=400, detail="Email уже занят")
    
    db_reader = Reader(**reader.model_dump())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

def get_reader(db: Session, reader_id: int):
    """Получить читателя по ID"""
    return db.query(Reader).filter(Reader.id == reader_id).first()

def get_reader_by_email(db: Session, email: str):
    """Получить читателя по email"""
    return db.query(Reader).filter(Reader.email == email).first()

def get_readers(db: Session, skip: int = 0, limit: int = 100):
    """Получить список всех читателей"""
    return db.query(Reader).offset(skip).limit(limit).all()

def update_reader(db: Session, reader_id: int, reader_update: schemas.ReaderUpdate):
    """Обновить данные читателя"""
    db_reader = get_reader(db, reader_id)
    if not db_reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    
    # Проверка уникальности email, если он изменен
    if reader_update.email and reader_update.email != db_reader.email:
        existing = db.query(Reader).filter(Reader.email == reader_update.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email уже занят")
    
    # Обновление полей
    for field, value in reader_update.model_dump(exclude_unset=True).items():
        setattr(db_reader, field, value)
    
    db.commit()
    db.refresh(db_reader)
    return db_reader

def delete_reader(db: Session, reader_id: int):
    """Удалить читателя"""
    db_reader = get_reader(db, reader_id)
    if not db_reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    
    db.delete(db_reader)
    db.commit()
    return {"message": "Читатель успешно удален"}

