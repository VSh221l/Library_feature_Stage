from app.models import Book
import logging

def test_borrow_book_success(client, db, create_test_book, create_test_reader, create_test_user):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/borrow/", json={"book_id": create_test_book.id, "reader_id": create_test_reader.id}, headers=headers)
    assert response.status_code == 200
    assert response.json()["book_id"] == create_test_book.id
    assert response.json()["return_date"] is None

    # Проверка уменьшения количества экземпляров
    book = client.get(f"/books/{create_test_book.id}", headers=headers).json()
    assert book.get("quantity") == 0

def test_borrow_book_no_copies(client, db, create_test_book, create_test_reader, create_test_user):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Уменьшаем количество до 0
    book = db.get(Book, create_test_book.id)
    book.quantity = 0
    db.commit()

    response = client.post("/borrow/", json={"book_id": create_test_book.id, "reader_id": create_test_reader.id}, headers=headers)
    assert response.status_code == 400
    assert "Книга недоступна для выдачи" in response.json()["detail"]

def test_return_book(client, db, create_test_book, create_test_user, create_test_reader):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Выдаём книгу
    borrow_response = client.post("/borrow/", json={"book_id": create_test_book.id, "reader_id": create_test_reader.id}, headers=headers)
    assert borrow_response.status_code == 200
    borrow_id = borrow_response.json()["id"]

    # Возвращаем
    response = client.post("/borrow/return", params={"borrow_id": borrow_id}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Книга успешно возвращена"

    # Проверка увеличения количества экземпляров
    book = client.get(f"/books/{create_test_book.id}", headers=headers).json()
    assert book.get("quantity") == 1

    # Повторный возврат
    response = client.post("/borrow/return", params={"borrow_id": borrow_id}, headers=headers)
    assert response.status_code == 400
    assert "Книга уже возвращена" in response.json()["detail"]

def test_borrow_max_books(client, db, create_test_book, create_test_user, create_test_reader):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Проверяем, что у читателя нет книг
    response = client.get(f"/borrow/reader/{create_test_reader.id}", headers=headers)
    assert len(response.json()) == 0

    response = client.post("/books/", json={"title": "Отрицательная книга", "author": "Автор", "quantity": 4}, headers=headers)
    # Assert the response status code
    assert response.status_code == 201, f"Неожиданный код ответа: {response.status_code}"

    # Assert the response contains the expected keys
    response_data = response.json()
    assert "id" in response_data, "Отсутствует ключ 'id'"
    created_book_id = response.json()["id"]

    for _ in range(3):
        response = client.post("/borrow/", json={"book_id": created_book_id, "reader_id": create_test_reader.id}, headers=headers)
        assert response.status_code == 200

    response = client.post("/borrow/", json={"book_id": created_book_id, "reader_id": create_test_reader.id}, headers=headers)
    assert response.status_code == 400
    assert "Превышено максимальное количество книг" in response.json()["detail"]