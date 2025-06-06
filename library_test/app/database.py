from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
# Асинхронная строка подключения

# Создаем асинхронный движок
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries
    pool_pre_ping=True  # Check connections before use
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Многопоточная безопасность
db_session = scoped_session(SessionLocal)

# Базовый класс для моделей
Base = declarative_base()
Base.query = db_session.query_property()

# Зависимость для FastAPI
def get_database():
    """
    Получить сессию базы данных.
    Используется как зависимость в FastAPI маршрутах.
    """
    db = db_session()
    try:
        yield db
    finally:
        db.close()