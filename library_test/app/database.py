from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение строки подключения из переменной окружения
# Пример: DATABASE_URL=postgresql://user:password@localhost/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Создаем движок SQLAlchemy
# pool_pre_ping=True помогает обрабатывать потерянные соединения с БД
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("postgresql") else {},
    pool_pre_ping=True
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Используем scoped_session для многопоточной безопасности
# Это гарантирует, что каждая сессия будет уникальна для потока/запроса
db_session = scoped_session(SessionLocal)

# Базовый класс для всех моделей
Base = declarative_base()
Base.query = db_session.query_property()

def get_database():
    """
    Получить сессию базы данных.
    Используется как зависимость в FastAPI маршрутах.
    """
    db = db_session()
    try:
        yield db  # Используем yield для корректного закрытия сессии после использования
    finally:
        db.close()