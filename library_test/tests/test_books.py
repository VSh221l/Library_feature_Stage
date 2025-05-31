def test_create_book(client):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Успешное создание
    response = client.post("/books/", json={"title": "Новая книга", "author": "Автор"}, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Новая книга"
    assert response.json()["quantity"] == 1

    # Проверка уникальности ISBN
    response = client.post("/books/", json={"title": "Еще книга", "author": "Автор", "isbn": "123-456"}, headers=headers)
    assert response.status_code == 201
    response = client.post("/books/", json={"title": "Дубль", "author": "Автор", "isbn": "123-456"}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "ISBN уже занят"

    # Проверка отрицательного количества
    response = client.post("/books/", json={"title": "Отрицательная книга", "author": "Автор", "quantity": -1}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Количество не может быть отрицательным"

def test_get_books_unprotected(client):
    response = client.get("/books/")
    assert response.status_code == 200

def test_update_book(client, create_test_book):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(f"/books/{create_test_book.id}", json={"title": "Обновленная книга"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Обновленная книга"

    # Попытка использовать занятый ISBN
    response = client.post("/books/", json={"title": "Книга 2", "author": "Автор", "isbn": "123-456"}, headers=headers)
    assert response.status_code == 201
    response = client.put(f"/books/{response.json()['id']}", json={"isbn": "123-456"}, headers=headers)
    assert response.status_code == 400
    assert "ISBN уже занят" in response.json()["detail"]

def test_delete_book(client, create_test_book):
    token = client.post("/auth/token", json={"email": "test@example.com", "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete(f"/books/{create_test_book.id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Книга успешно удалена"}