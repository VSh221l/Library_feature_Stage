# Библиотечная система API

## Запуск проекта
1. Установите зависимости: `pip install -r requirements.txt`
2. Создайте базу данных PostgreSQL:
   ```sql
   CREATE USER library_user WITH PASSWORD 'password';
   CREATE DATABASE library_db OWNER library_user;
3. cp .env.example .env
# Отредактируйте .env с вашими учетными данными БД
4. Примените миграции: alembic upgrade head
5. Запустите сервер: uvicorn app.main:app --reload

## Регистрация первого пользователя:
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@example.com", "password": "admin123"}'

## Структура проекта
library_api/
├─ alembic/                # Миграции БД
├─ app/
│   ├─ crud/
│      ├─ crud_books.py    # CRUD-операции и вспомогательные функции для книг
│      ├─ crud_readers.py  # CRUD-операции и вспомогательные функции для читателей
│   ├─ models.py           # ORM-модели SQLAlchemy
│   ├─ schemas.py          # Pydantic-схемы валидации
│   ├─ database.py         # Подключение к БД
│   ├─ auth.py             # JWT-аутентификация
│   ├─ crud.py             # Логика работы с БД
│   ├─ routers/            # Роутеры FastAPI
│   └─ main.py             # Точка входа
├─ tests/                  # Тесты
└─ README.md               # Документация
## Структура БД
users : Пользователи (библиотекари)
id (PK), email (UNIQUE), hashed_password
books : Книги
id (PK), title, author, year, isbn (UNIQUE), quantity
readers : Читатели
id (PK), name, email (UNIQUE)
borrowed_books : Выдачи книг
id (PK), book_id (FK), reader_id (FK), borrow_date, return_date

## Выбор решений:
quantity в таблице books позволяет избежать лишних JOIN при проверке доступности.
Отдельная таблица borrowed_books хранит историю выдач.
isbn и email уникальны для предотвращения дубликатов.

## Аутентификация
JWT : Генерируются с помощью python-jose, срок жизни 30 минут.
Хеширование : Пароли хранятся через bcrypt (библиотека passlib[bcrypt]).
Защищенные эндпоинты : Все, кроме /auth/register и /auth/token.

Почему так?
python-jose поддерживает алгоритмы шифрования (HS256).
bcrypt безопасен для хранения паролей (медленные хэши).

### Выбор в пользу аутетификации при доступе к книгам
Выбор обусловлен сделан из соображений логики созданного сервиса: система предназначена для библиотекарей, потому нет смысла предоставлять публичный доступ к изначально закрытому ресурсу.

## Дополнительная фича: Уведомления о сроках возврата
Реализация:

Добавить поле due_date в borrowed_books (по умолчанию +14 дней от borrow_date).
Планировщик задач (например, Celery Beat) будет проверять просроченные книги.
При обнаружении просрочки отправлять email читателю через SMTP-сервис.