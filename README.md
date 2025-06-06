# Библиотечная система API

## Запуск проекта

### Установка

0. Скопируйте содержимое репозитория:
   ```bash
   git clone https://github.com/your-repo/library_api.git
   cd library_api

1. Установите зависимости: `pip install -r requirements.txt`
2. Создайте базу данных PostgreSQL:
   ```sql
   CREATE USER library_user WITH PASSWORD 'password';
   CREATE DATABASE library_db OWNER library_user;
3. Создайте и отредактируйте .env с вашими учетными данными БД
4. Запустите Docker-контейнер командой: `docker-compose up`
5. Примените миграции: `alembic upgrade head`
6. Запустите сервер: `uvicorn app.main:app --reload`

## Регистрация первого пользователя:
   ```bash
   curl -X POST "http://localhost:8000/auth/register" \
   -H "Content-Type: application/json" \
   -d '{"email": "admin@example.com", "password": "admin123"}'
   ```

## Структура проекта
```
library_api/
├── alembic/                # Database migrations
├── app/
│   ├── crud/               # CRUD operations and helper functions
│   │   ├── crud_books.py   # CRUD for books
│   │   ├── crud_readers.py # CRUD for readers
│   ├── models.py           # SQLAlchemy ORM models
│   ├── schemas.py          # Pydantic validation schemas
│   ├── database.py         # Database connection and session management
│   ├── auth.py             # JWT authentication logic
│   ├── routers/            # FastAPI routers
│   │   ├── books.py        # Endpoints for books
│   │   ├── readers.py      # Endpoints for readers
│   │   ├── auth.py         # Endpoints for authentication
│   └── main.py             # Application entry point
├── tests/                  # Unit and integration tests
│   ├── test_books.py       # Tests for book-related functionality
│   ├── test_readers.py     # Tests for reader-related functionality
│   ├── test_auth.py        # Tests for authentication
│   └── test_borrowing_books.py # Tests for borrowing functionality
├── .env.example            # Example environment configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Структура БД
Схема базы данных состоит из следующих таблиц:

users: пользователи
id (PK): Уникальный идентификатор пользователя.
email (UNIQUE): Адрес электронной почты пользователя.
hashed_password: Хешированный пароль для аутентификации.

books: книги
id (PK): Уникальный идентификатор книги.
title (PK): Название книги.
автор: Автор книги.
год: Год публикации.
isbn (UNIQUE): ISBN книги.
количество: Количество доступных экземпляров.

readers: читатели
id (PK): Уникальный идентификатор читателя.
name: Имя читателя.
email (UNIQUE): Адрес электронной почты читателя.

borrowed_books: оформленные_книги
id (PK): Уникальный идентификатор записи о заимствовании.
book_id (FK): Внешний ключ, ссылающийся на таблицу books.
reader_id (FK): Внешний ключ, ссылающийся на таблицу читателей.
borrow_date: Дата, когда книга была взята на время.
return_date: Дата, когда книга была возвращена.

## Выбор решений:
* quantity в таблице books позволяет избежать лишних JOIN при проверке доступности.
* Отдельная таблица borrowed_books хранит историю выдач.
* isbn и email уникальны для предотвращения дубликатов.

## Аутентификация
JWT : Генерируются с помощью python-jose, срок жизни 30 минут.
Хеширование : Пароли хранятся через bcrypt (библиотека passlib[bcrypt]).
Защищенные эндпоинты : Все, кроме /auth/register и /auth/token.

Почему так?
- python-jose поддерживает алгоритмы шифрования (HS256).
- bcrypt безопасен для хранения паролей (медленные хэши).

### Выбор в пользу аутетификации при доступе к книгам
Выбор обусловлен сделан из соображений логики созданного сервиса: система предназначена для библиотекарей, потому нет смысла предоставлять публичный доступ к изначально закрытому ресурсу.

## Дополнительная фича: Уведомления о сроках возврата
### Реализация:
Добавить поле due_date в borrowed_books (по умолчанию +14 дней от borrow_date).
Планировщик задач (например, Celery Beat) будет проверять просроченные книги.
При обнаружении просрочки отправлять email читателю через SMTP-сервис.