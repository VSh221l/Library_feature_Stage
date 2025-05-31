import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base
from sqlalchemy.orm import sessionmaker
from app.models import User, Book, Reader, BorrowedBook

# Создание тестового клиента
@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

# Создание тестовой сессии
@pytest.fixture(scope="function")
def db():
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()

# Создание тестового пользователя
@pytest.fixture
def create_test_user(db):
    from app.auth import get_password_hash
    user = User(email="test@example.com", hashed_password=get_password_hash("password123"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Создание тестовой книги
@pytest.fixture
def create_test_book(db):
    book = Book(title="Test Book", author="Test Author", quantity=1)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

# Создание тестового читателя
@pytest.fixture
def create_test_reader(db):
    reader = Reader(name="Test Reader", email="reader@example.com")
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader