import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base, db_session, SessionLocal
from app.models import User, Book, Reader, BorrowedBook

# Создание тестового клиента
@pytest.fixture(scope="function", autouse=True)
def client():
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    try:
        yield client  # получаем настоящую сессию
    finally:
        db_session.remove()  # Ensure the database session is cleaned up
        Base.metadata.drop_all(bind=engine)  # Drop tables after tests (optional)


# Создание тестовой сессии
@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # Откат транзакции после каждого теста
        db.close()


# Создание тестового пользователя
@pytest.fixture(scope="function")
def create_test_user(db):
    from app.auth import get_password_hash

    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == "test@example.com").first()
    if existing_user:
        return existing_user

    # Создание нового пользователя
    # email = f"test_{uuid.uuid4().hex}@example.com"
    email = "test@example.com"
    user = User(email=email, hashed_password=get_password_hash("password123"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Создание тестовой книги
@pytest.fixture(scope="function")
def create_test_book(db):
    book = Book(title="Test Book", author="Test Author", quantity=1)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

# Создание тестового читателя
@pytest.fixture(scope="function")
def create_test_reader(db):

    # Check if the user already exists
    reader = db.query(Reader).filter(Reader.email == "reader@example.com").first()
    if reader:
        return reader

    reader = Reader(name="Test Reader", email="reader@example.com")
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader
