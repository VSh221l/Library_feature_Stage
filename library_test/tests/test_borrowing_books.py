from app.models import Book

def test_borrow_book_success(client, db, create_test_book, create_test_reader):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/borrow/", json={"book_id": create_test_book.id, "reader_id": create_test_reader.id}, headers=headers)
    assert response.status_code == 200
    assert response.json()["book_id"] == create_test_book.id
    assert response.json()["return_date"] is None

    # Проверка уменьшения количества экземпляров
    book = db.query(Book).get(create_test_book.id) 
    assert book.quantity == 0

def test_borrow_book_no_copies(client, db, create_test_book, create_test_reader, create_test_user):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Уменьшаем количество до 0
    book = db.query(Book).get(create_test_book.id)
    book.quantity = 0
    db.commit()

    response = client.post("/borrow/", json={"book_id": create_test_book.id, "reader_id": create_test_reader.id}, headers=headers)
    assert response.status_code == 400
    assert "Книга недоступна для выдачи" in response.json()["detail"]

def test_borrow_max_books(client, db, create_test_book, create_test_reader, create_test_user):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    for _ in range(3):
        response = client.post("/borrow/", json={"book_id": create_test_book.id, "reader_id": create_test_reader.id}, headers=headers)
        assert response.status_code == 200

    response = client.post("/borrow/", json={"book_id": create_test_book.id, "reader_id": create_test_reader.id}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Превышено максимальное количество книг"

def test_return_book(client, db, create_test_book, create_test_reader, create_test_user):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Выдаём книгу
    borrow_response = client.post("/borrow/", json={"book_id": create_test_book.id, "reader_id": create_test_reader.id}, headers=headers)
    assert borrow_response.status_code == 200
    borrow_id = borrow_response.json()["id"]

    # Возвращаем
    response = client.post("/borrow/return", json={"borrow_id": borrow_id}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Книга успешно возвращена"

    # Проверка увеличения количества
    book = db.query(Book).get(create_test_book.id)
    assert book.quantity == 1

    # Повторный возврат
    response = client.post("/borrow/return", json={"borrow_id": borrow_id}, headers=headers)
    assert response.status_code == 400
    assert "Книга уже возвращена" in response.json()["detail"]