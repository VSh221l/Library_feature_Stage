from fastapi import APIRouter, Depends, HTTPException, status
from app import auth
from sqlalchemy.orm import Session
from app.models import User
from app import database, schemas

# Роутер для аутентификации
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# --- Эндпоинты ---

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserLogin, db: Session = Depends(database.get_database)):
    """
    Регистрация нового пользователя (библиотекаря).
    Проверяет уникальность email и хеширует пароль.
    """
    # Проверка, существует ли пользователь
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )
    
    # Хеширование пароля
    hashed_password = auth.get_password_hash(user.password)
    
    # Создание пользователя
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Пользователь успешно зарегистрирован"}

@router.post("/token")
def login(user: schemas.UserLogin, db: Session = Depends(database.get_database)):
    """
    Аутентификация пользователя.
    Возвращает JWT-токен, если email и пароль верны.
    """
    # Поиск пользователя в БД
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Генерация токена
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}